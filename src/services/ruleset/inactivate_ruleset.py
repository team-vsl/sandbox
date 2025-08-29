# Import built-in libraries
import os
import sys

# Import 3rd-party libraries
import requests

# Import from utils
import utils.exceptions as Exps
from utils.constants import (
    RULESET_BUCKET_NAME,
    RULESET_MAPPING_DYNAMODB_TABLE_NAME,
)
from utils.dynamodb import update_item, query_item
from utils.rl_state import RulesetState
from utils.s3 import move_file
from utils.glue import update_inline_ruleset_in_job
from utils.helpers.boolean import check_empty_or_throw_error


def inactivate_ruleset(params):
    """
    Activate a inactive ruleset

    Args:
        params (dict): Parameters of this function.

    Returns:
        dict: response from activate_ruleset
    """
    path_params = params.get("path_params")
    query = params.get("query")
    body = params.get("body")
    headers = params.get("headers")
    meta = params.get("meta", {})

    ruleset_name = path_params.get("ruleset_name", "")
    version = body.get("version", "")

    check_empty_or_throw_error(
        version,
        "version",
        "Version of data contract must be specified to update its metadata",
    )

    ruleset_metadata = query_item(
        table_name=RULESET_MAPPING_DYNAMODB_TABLE_NAME,
        partition_query={"key": "name", "value": ruleset_name},
        sort_query={"key": "version", "value": version},
    )

    if ruleset_metadata is None or not ruleset_metadata:
        raise Exps.BadRequestException("The ruleset is not found to inactive")

    if ruleset_metadata.get("state") == RulesetState.Inactive:
        raise Exps.BadRequestException("The ruleset is already inactive")

    default_ext = "txt"
    old_state = RulesetState.Active
    new_state = RulesetState.Inactive
    source_object_key = f"{old_state}/{ruleset_name}.{default_ext}"
    dest_object_key = f"{new_state}/{ruleset_name}.{default_ext}"

    # Move object from /pending to /approved
    move_file(
        bucket_name=RULESET_BUCKET_NAME,
        source_key=source_object_key,
        dest_bucket_name=RULESET_BUCKET_NAME,
        dest_key=dest_object_key,
    )

    # Update corresponding dynamodb item (by name - pk and version - sk)
    updated_item = update_item(
        table_name=RULESET_MAPPING_DYNAMODB_TABLE_NAME,
        partition_query={"key": "name", "value": ruleset_name},
        sort_query={"key": "version", "value": version},
        data={"state": new_state, "job_name": ""},
    )

    update_inline_ruleset_in_job(
        job_name=ruleset_metadata.get("job_name"),
        new_ruleset='Rules = [ColumnExists "id"]',
    )

    return updated_item
