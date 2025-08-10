# Import built-in libraries
import os
import sys

# Import 3rd-party libraries
import requests

# Import from utils
from utils.glue import list_jobs


def list_etl_jobs(params):
    """
    List available jobs.

    Args:
        params (dict): Parameters of this function.

    Returns:
        dict: result from list_jobs.
    """
    path_params = params.get("path_params")
    query = params.get("query")
    body = params.get("body")
    headers = params.get("headers")
    meta = params.get("meta", {})

    result = list_jobs(limit=query.get("limit", 10))

    return result
