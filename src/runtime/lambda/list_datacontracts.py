# Import built-in libraries
import traceback, os

# Import 3rd-party libraries

# Import utils
import utils.exceptions as Exps
from utils.helpers import request as request_helpers
from utils.logger import get_logger
from utils.response_builder import ResponseBuilder


async def handler(event, context):
    rb = ResponseBuilder()
    logger = get_logger()

    try:
        # Extract request data
        claims = request_helpers.get_claims_from_event(event)
        pathParams = request_helpers.get_path_params_from_event(event)
        body = request_helpers.get_body_from_event(event)

        # Return response
        rb.set_status_code(200)
        rb.set_data({})

        return rb.create_response()
    except Exps.AppException as error:
        logger.error("Error | [list_datacontracts]:", error)
        return rb.create_error_response(error)
    except Exps.InternalException as error:
        error.message = (
            "There is an internal error in server Contact with Admin to get support."
        )
        logger.error("Error | [list_datacontracts]:", error)
        return rb.create_error_response(error)
    except Exception as error:
        logger.error(
            "Uknown error | [list_datacontracts]:", error, traceback.format_exc()
        )
        error.message = (
            "There is an internal error in server Contact with Admin to get support."
        )
        return rb.create_error_response(Exps.UnknownException(str(error)))
    finally:
        logger.debug("End execution of [list_datacontracts]")
