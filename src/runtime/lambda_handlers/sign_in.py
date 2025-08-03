# Import built-in libraries
import traceback, os

# Import 3rd-party libraries

# Import from authorizer
from authorizer import sign_in, sign_in_with_id_token

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

        id_token = body.get("idToken")

        if id_token:
            response = sign_in_with_id_token(id_token=id_token)
        else:
            response = await sign_in(
                username=body.get("username"),
                email=body.get("email"),
                password=body.get("password"),
            )

        # Return response
        rb.set_status_code(200)
        rb.set_data(response)

        return rb.create_response()
    except Exps.AppException as error:
        logger.error(f"Error | [sign_in]: {error}")
        return rb.create_error_response(error)
    except Exps.InternalException as error:
        error.message = (
            "There is an internal error in server Contact with Admin to get support."
        )
        logger.error(f"Error | [sign_in]: {error}")
        return rb.create_error_response(error)
    except Exception as error:
        logger.error(f"Uknown error | [sign_in]: {error} {traceback.format_exc()}")
        error.message = (
            "There is an internal error in server Contact with Admin to get support."
        )
        return rb.create_error_response(Exps.UnknownException(str(error)))
    finally:
        logger.debug("End execution of [sign_in]")
