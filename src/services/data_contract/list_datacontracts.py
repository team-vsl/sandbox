# Import built-in libraries

# Import 3rd-party libraries

# Import from utils
from utils.constants import (
    RULESET_MAPPING_DYNAMODB_TABLE_NAME,
    RULESET_DYNAMODB_STATE_GSI_NAME,
)
from utils.s3 import list_files
from utils.dynamodb import query_items_with_gsi
from utils.helpers.other import convert_keys_to_camel_case


def list_datacontracts(params):
    """List data contracts from bucket

    Args:
        params (dict): parameters of this function

    Returns:
        dict: result from list objects
    """
    path_params, query, body, headers, meta = (
        params.get("path_params"),
        params.get("query"),
        params.get("body"),
        params.get("headers"),
        params.get("meta", {}),
    )

    state = query.get("state")

    result = query_items_with_gsi(
        table_name=RULESET_MAPPING_DYNAMODB_TABLE_NAME,
        index_name=RULESET_DYNAMODB_STATE_GSI_NAME,
        partition_query={"key": "state", "value": state},
    )

    return convert_keys_to_camel_case(result)
