# Import built-in libraries
import os
import io
import sys
from datetime import datetime, timezone

# Import 3rd-party libraries
import requests
import yaml

# Import from utils
from utils.constants import (
    RULESET_BUCKET_NAME,
    RULESET_MAPPING_DYNAMODB_TABLE_NAME,
)
from utils.rl_state import RulesetState
from utils.s3 import upload_fileobj
from utils.dynamodb import add_item
from utils.helpers.boolean import check_empty_or_throw_error


def upload_ruleset(params):
    """
    Upload a ruleset to s3, new ruleset will be uploaded to /inactive folder

    Args:
        params (dict): Parameters of this function.

    Returns:
        dict: metadata of rulest
    """
    path_params = params.get("path_params")
    query = params.get("query")
    body = params.get("body")
    headers = params.get("headers")
    meta = params.get("meta", {})

    claims = meta.get("claims", {})
    content = body.get("content", "")
    name = body.get("name", "")
    version = version.get("version", "")

    check_empty_or_throw_error(
        content,
        "content",
        "Content of rulest is required to upload ruleset",
    )
    check_empty_or_throw_error(
        name,
        "name",
        "Name of rulest is required to upload ruleset",
    )
    check_empty_or_throw_error(
        version,
        "version",
        "Version of rulest is required to upload ruleset",
    )

    teams = claims.get("cognito:groups", [])

    ruleset_meta = {
        "name": name,
        "version": version,
        "state": RulesetState.Inactive,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "owner": claims.get("username", ""),
        "team": teams[0] if len(teams) > 0 else "",
    }

    check_empty_or_throw_error(ruleset_meta.get("name"), "ruleset_name")
    check_empty_or_throw_error(ruleset_meta.get("version"), "ruleset_version")
    check_empty_or_throw_error(ruleset_meta.get("owner"), "ruleset_owner")
    check_empty_or_throw_error(ruleset_meta.get("team"), "ruleset_team")

    # Upload file
    default_ext = "txt"
    object_key = f"{RulesetState.Inactive}/{ruleset_meta.get("name")}.{default_ext}"
    bytes = io.BytesIO(content.encode("utf-8"))
    url = upload_fileobj(
        bytes=bytes,
        bucket_name=RULESET_BUCKET_NAME,
        object_name=object_key,
        metadata={
            "owner": ruleset_meta.get("owner"),
            "team": ruleset_meta.get("team"),
        },
    )

    # Save metadata
    add_item(table_name=RULESET_MAPPING_DYNAMODB_TABLE_NAME, data=ruleset_meta)

    return ruleset_meta
