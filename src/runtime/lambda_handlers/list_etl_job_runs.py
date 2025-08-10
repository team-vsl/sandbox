# Import built-in libraries
import traceback
import os

# Import utils
import utils.exceptions as Exps
from utils.helpers import request as request_helpers
from utils.helpers.other import convert_keys_to_camel_case
from utils.logger import get_logger
from utils.response_builder import ResponseBuilder

from services.job import list_etl_job_runs


async def handler(event, context):
    rb = ResponseBuilder()
    logger = get_logger()

    try:
        # Extract request data
        claims = request_helpers.get_claims_from_event(event)
        path_params = request_helpers.get_path_params_from_event(event)
        query = request_helpers.get_query_from_event(event)
        body = request_helpers.get_body_from_event(event)

        result = list_etl_job_runs({"path_params": path_params, "query": query})

        # Return response
        rb.set_status_code(200)
        rb.set_data(result.get("job_runs", []))
        rb.set_metadata(convert_keys_to_camel_case(result.get("meta", {})))

        return rb.create_response()

    except Exps.AppException as error:
        logger.error(f"Error | [list_etl_job_runs]: {error}")
        return rb.create_error_response(error)

    except Exception as error:
        logger.error(
            f"Unknown error | [list_etl_job_runs]: {error} {traceback.format_exc()}"
        )
        return rb.create_error_response(Exps.UnknownException(str(error)))

    finally:
        logger.debug("End execution of [list_etl_job_runs]")
