# Import built-in libraries
import traceback

# Import utils
import utils.exceptions as Exps
from utils.helpers import request as request_helpers
from utils.logger import get_logger
from utils.response_builder import ResponseBuilder

# Import services
from services.ruleset import upload_ruleset


async def handler(event, context):
    rb = ResponseBuilder()
    logger = get_logger()

    try:
        # Extract request data
        claims = request_helpers.get_claims_from_event(event)
        path_params = request_helpers.get_path_params_from_event(event)
        body = request_helpers.get_body_from_event(event)

        # Upload ruleset
        response = upload_ruleset({"body": body, "meta": {"claims": claims}})

        rb.set_status_code(200)
        rb.set_data(response)
        return rb.create_response()
    except Exps.AppException as error:
        logger.error(f"Error | [upload_ruleset]: {error}")
        return rb.create_error_response(error)
    except Exps.InternalException as error:
        error.message = (
            "There is an internal error in server Contact with Admin to get support."
        )
        logger.error(f"Error | [upload_ruleset]: {error}")
        return rb.create_error_response(error)
    except Exception as error:
        logger.error(
            f"Uknown error | [upload_ruleset]: {error} {traceback.format_exc()}"
        )
        error.message = (
            "There is an internal error in server Contact with Admin to get support."
        )
        return rb.create_error_response(Exps.UnknownException(str(error)))
    finally:
        logger.debug("End execution of [upload_ruleset]")
