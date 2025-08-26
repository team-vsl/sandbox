# Import built-in libraries
import os
import sys

# Import 3rd-party libraries
import requests

# Import services
from services.data_contract import get_datacontract
from services.ruleset import upload_ruleset, generate_ruleset

# Import from utils
from utils.constants import (
    DATACONTRACT_BUCKET_NAME,
    DATACONTRACT_MAPPING_DYNAMODB_TABLE_NAME,
)
from utils.dc_state import DataContractState
from utils.rl_state import RulesetState
from utils.dynamodb import update_item
from utils.s3 import move_file, upload_fileobj
from utils.helpers.boolean import check_empty_or_throw_error


def approve_datacontract(params):
    """
    Approve a pending data contract

    Args:
        params (dict): Parameters of this function.

    Returns:
        dict: response from approve_datacontract
    """
    path_params = params.get("path_params")
    query = params.get("query")
    body = params.get("body")
    headers = params.get("headers")
    meta = params.get("meta", {})

    object_name = path_params.get("datacontract_name", "")
    version = body.get("version", "")

    check_empty_or_throw_error(
        version,
        "version",
        "Version of data contract must be specified to update its metadata",
    )

    default_ext = "yaml"
    old_state = DataContractState.Pending
    new_state = DataContractState.Approved
    source_object_key = f"{old_state}/{object_name}.{default_ext}"
    dest_object_key = f"{new_state}/{object_name}.{default_ext}"

    # Move object from /pending to /approved
    move_file(
        bucket_name=DATACONTRACT_BUCKET_NAME,
        source_key=source_object_key,
        dest_bucket_name=DATACONTRACT_BUCKET_NAME,
        dest_key=dest_object_key,
    )

    # Update corresponding dynamodb item (by name - pk and version - sk)
    updated_item = update_item(
        table_name=DATACONTRACT_MAPPING_DYNAMODB_TABLE_NAME,
        partition_query={"key": "name", "value": object_name},
        sort_query={"key": "version", "value": version},
        data={"state": new_state},
    )

    # Get content of data contract
    data_contract_raw = get_datacontract(
        {
            "path_params": {"name": object_name},
            "query": {"state": new_state},
            "meta": meta,
        }
    )
    data_contract_content = data_contract_raw.read().decode("utf-8")

    # Generate ruleset
    ruleset_content = generate_ruleset({"body": {"content": data_contract_content}})

    # Upload ruleset
    ruleset_name = f"{object_name} Ruleset"
    ruleset_version = "1.0.0"

    upload_ruleset(
        {
            "body": {
                "name": ruleset_name,
                "content": ruleset_content,
                "version": ruleset_version,
            },
            "meta": meta,
        }
    )

    return {"dataContractInfo": updated_item, "rulesetName": ruleset_name}
