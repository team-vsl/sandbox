# Import built-in libraries
import os
import sys

# Import 3rd-party libraries
import requests

# Import from utils
import utils.exceptions as Exps
from utils.constants import DATACONTRACT_BUCKET_NAME
from utils.s3 import get_file_meta
from utils.helpers.data_contract import transform_dc_res_from_head_api


def get_datacontract_info(params):
    """
    Get information of a data contract (s3 object's metadata)

    Args:
        params (dict): Parameters of this function.

    Returns:
        dict: information of data contract
    """
    path_params = params.get("path_params")
    query = params.get("query")
    body = params.get("body")
    headers = params.get("headers")
    meta = params.get("meta", {})

    default_ext = "yaml"
    name = path_params.get("name")
    state = query.get("state")

    if state is None:
        raise Exps.BadRequestException(
            "State of object is required when get data contract's information"
        )

    object_key = f"{state}/{name}.{default_ext}"

    file_meta = get_file_meta(
        bucket_name=DATACONTRACT_BUCKET_NAME, object_key=object_key
    )

    result = transform_dc_res_from_head_api(file_meta)
    result["name"] = name
    result["state"] = state

    return result
