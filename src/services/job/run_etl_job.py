# Import built-in libraries
import os
import sys

# Import 3rd-party libraries
import requests

# Import from utils
from utils.glue import start_job


def run_etl_job(params):
    """
    Run an available job

    Args:
        params (dict): Parameters of this function.

    Returns:
        dict: result from start_job.
    """
    path_params = params.get("path_params")
    query = params.get("query")
    body = params.get("body")
    headers = params.get("headers")
    meta = params.get("meta", {})

    result = start_job(job_name=path_params.get("job_name"))

    return {"jobRunId": result}
