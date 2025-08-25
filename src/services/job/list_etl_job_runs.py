# Import built-in libraries
import os
import sys

# Import 3rd-party libraries
import requests

# Import from utils
from utils.glue import list_job_runs


def list_etl_job_runs(params):
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

    result = list_job_runs(
        job_name=path_params.get("job_name"), limit=int(query.get("limit", "10"))
    )

    return result
