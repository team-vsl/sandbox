# Import built-in libraries
import os
import sys

# Import 3rd-party libraries
import requests

# Import from utils
import utils.exceptions as Exps
from utils.constants import RULESET_MAPPING_DYNAMODB_TABLE_NAME
from utils.s3 import get_file_meta
from utils.dynamodb import query_item
from utils.helpers.data_contract import transform_dc_res_from_head_api
from utils.helpers.other import convert_keys_to_camel_case


def get_ruleset_info(params):
    """
    Get information of a ruleset (from dynamodb)

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

    name = path_params.get("name")

    result = query_item(
        table_name=RULESET_MAPPING_DYNAMODB_TABLE_NAME,
        partition_query={"key": "name", "value": name},
    )

    return convert_keys_to_camel_case(result)
