# Import built-in libraries
import traceback, os

# Import 3rd-party libraries

# Import utils
import utils.exceptions as Exps
from utils.helpers import request as request_helpers
from utils.logger import get_logger
from utils.response_builder import ResponseBuilder

from utils.glue import get_job


async def handler(event, context):
    rb = ResponseBuilder()
    logger = get_logger()

    try:
        # Extract request data
        claims = request_helpers.get_claims_from_event(event)
        path_params = request_helpers.get_path_params_from_event(event)
        body = request_helpers.get_body_from_event(event)

        response = get_job(job_name=path_params.get("job_name"))

        # Return response
        rb.set_status_code(200)
        rb.set_data(response)

        return rb.create_response()
    except Exps.AppException as error:
        logger.error(f"Error | [get_etl_job]: {error}")
        return rb.create_error_response(error)
    except Exps.InternalException as error:
        error.message = (
            "There is an internal error in server Contact with Admin to get support."
        )
        logger.error(f"Error | [get_etl_job]: {error}")
        return rb.create_error_response(error)
    except Exception as error:
        logger.error(f"Uknown error | [get_etl_job]: {error} {traceback.format_exc()}")
        error.message = (
            "There is an internal error in server Contact with Admin to get support."
        )
        return rb.create_error_response(Exps.UnknownException(str(error)))
    finally:
        logger.debug("End execution of [get_etl_job]")
