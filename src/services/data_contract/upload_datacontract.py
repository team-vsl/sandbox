# Import built-in libraries
import os
import io
import sys
import time
from datetime import datetime, timezone

# Import 3rd-party libraries
import requests
import yaml

# Import from utils
from utils.constants import (
    DATACONTRACT_BUCKET_NAME,
    DATACONTRACT_MAPPING_DYNAMODB_TABLE_NAME,
)
from utils.dc_state import DataContractState
from utils.s3 import upload_fileobj
from utils.dynamodb import add_item
from utils.helpers.boolean import check_empty_or_throw_error


def upload_datacontract(params):
    """
    Upload a data contract to s3, new data contract will
    be uploaded to /pending folder

    Args:
        params (dict): Parameters of this function.

    Returns:
        dict: metadata of data contract
    """
    path_params = params.get("path_params")
    query = params.get("query")
    body = params.get("body")
    headers = params.get("headers")
    meta = params.get("meta", {})

    claims = meta.get("claims", {})
    content = body.get("content", "")

    check_empty_or_throw_error(
        content,
        "content",
        "Content of data contract is required to upload data contract",
    )

    content_data = yaml.safe_load(content)

    name = content_data.get("title", f"Untitled Data Contract - {time.time() * 1000}")
    version = content_data.get("version", "1.0.0")

    info = content_data.get("metainfo")
    if isinstance(info, dict):
        name = info.get("title", name)
        version = info.get("version", version)

    teams = claims.get("cognito:groups", [])

    datacontract_meta = {
        "name": name,
        "version": version,
        "state": DataContractState.Pending,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "owner": claims.get("username", ""),
        "team": teams[0] if len(teams) > 0 else "",
    }

    check_empty_or_throw_error(datacontract_meta.get("name"), "datacontract_name")
    check_empty_or_throw_error(datacontract_meta.get("version"), "datacontract_version")
    check_empty_or_throw_error(datacontract_meta.get("owner"), "datacontract_owner")
    check_empty_or_throw_error(datacontract_meta.get("team"), "datacontract_team")

    # Upload file
    default_ext = "yaml"
    object_key = (
        f"{DataContractState.Pending}/{datacontract_meta.get("name")}.{default_ext}"
    )
    bytes = io.BytesIO(content.encode("utf-8"))
    url = upload_fileobj(
        fileobj=bytes,
        bucket_name=DATACONTRACT_BUCKET_NAME,
        object_name=object_key,
        metadata={
            "owner": datacontract_meta.get("owner"),
            "team": datacontract_meta.get("team"),
        },
    )

    # Save metadata
    add_item(
        table_name=DATACONTRACT_MAPPING_DYNAMODB_TABLE_NAME, data=datacontract_meta
    )

    return datacontract_meta
