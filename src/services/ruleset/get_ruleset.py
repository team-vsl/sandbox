# Import built-in libraries

# Import 3rd-party libraries

# Import from utils
from utils.s3 import get_file
from utils.constants import RULESET_BUCKET_NAME


def get_ruleset(params):
    """Get content of ruleset

    Args:
        params (dict): parameters of this function

    Returns:
        Any: streaming response
    """
    path_params, query, body, headers, meta = (
        params.get("path_params"),
        params.get("query"),
        params.get("body"),
        params.get("headers"),
        params.get("meta", {}),
    )

    default_ext = "txt"
    name = path_params.get("name")
    state = query.get("state")

    object_key = f"{state}/{name}.{default_ext}"

    file = get_file(bucket_name=RULESET_BUCKET_NAME, object_key=object_key)

    return file.get("Body")
