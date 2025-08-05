# Import built-in libraries

# Import 3rd-party libraries

# Import from utils
from utils.s3 import list_files
from utils.constants import DATACONTRACT_BUCKET_NAME
from utils.helpers.data_contract import transform_dc_res_from_list_api


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

    files = list_files(bucket_name=DATACONTRACT_BUCKET_NAME, prefix=state)

    return [transform_dc_res_from_list_api(file) for file in files[1:]]
