# Import built-in libraries
import traceback
import os

# Import utils
import utils.exceptions as Exps
from utils.helpers import request as request_helpers
from utils.logger import get_logger
from utils.response_builder import ResponseBuilder

from services.ruleset import get_ruleset_info


async def handler(event, context):
    rb = ResponseBuilder()
    logger = get_logger()

    try:
        # Extract request data
        claims = request_helpers.get_claims_from_event(event)
        path_params = request_helpers.get_path_params_from_event(event)
        query = request_helpers.get_query_from_event(event)
        body = request_helpers.get_body_from_event(event)

        response = get_ruleset_info({"path_params": path_params})

        # Return response
        rb.set_status_code(200)
        rb.set_data(response)

        return rb.create_response()

    except Exps.AppException as error:
        logger.error(f"Error | [get_ruleset_info]: {error}")
        return rb.create_error_response(error)

    except Exception as error:
        logger.error(
            f"Unknown error | [get_ruleset_info]: {error} {traceback.format_exc()}"
        )
        return rb.create_error_response(Exps.UnknownException(str(error)))

    finally:
        logger.debug("End execution of [get_ruleset_info]")
