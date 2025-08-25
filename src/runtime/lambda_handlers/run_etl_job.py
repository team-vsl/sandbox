# Import built-in libraries
import traceback

# Import 3rd-party libraries

# Import utils
import utils.exceptions as Exps
from utils.helpers import request as request_helpers
from utils.logger import get_logger
from utils.response_builder import ResponseBuilder

from services.job import run_etl_job


def handler(event, context):
    rb = ResponseBuilder()
    logger = get_logger()

    try:
        # Extract request data
        claims = request_helpers.get_claims_from_event(event)
        path_params = request_helpers.get_path_params_from_event(event)
        body = request_helpers.get_body_from_event(event)

        response = run_etl_job({"path_params": path_params.get("job_name")})

        # Return response
        rb.set_status_code(200)
        rb.set_data(response)

        return rb.create_response()
    except Exps.AppException as error:
        logger.error(f"Error | [run_etl_job]: {error}")
        return rb.create_error_response(error)
    except Exception as error:
        logger.error(f"Uknown error | [run_etl_job]: {error} {traceback.format_exc()}")
        return rb.create_error_response(Exps.UnknownException(str(error)))
    finally:
        logger.debug("End execution of [run_etl_job]")
