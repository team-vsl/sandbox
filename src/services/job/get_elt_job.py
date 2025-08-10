# Import built-in libraries
import os
import sys

# Import 3rd-party libraries
import requests

# Import from utils
from utils.glue import get_job


def get_etl_job(params):
    """
    Get ETL Job from Amazon Glue

    Args:
        params (dict): Parameters of this function.

    Returns:
        dict: Result from this function.
    """
    path_params = params.get("path_params")
    query = params.get("query")
    body = params.get("body")
    headers = params.get("headers")
    meta = params.get("meta", {})

    response = get_job(job_name=path_params.get("job_name"))

    return response
