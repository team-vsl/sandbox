# Import built-in libraries
import traceback

# Import utils
import utils.exceptions as Exps
from utils.helpers import request as request_helpers
from utils.logger import get_logger
from utils.response_builder import ResponseBuilder
from utils.ruleset_s3 import upload_ruleset


async def handler(event, context):
    rb = ResponseBuilder()
    logger = get_logger()

    try:
        # Extract request data
        pathParams = request_helpers.get_path_params_from_event(event)
        body = request_helpers.get_body_from_event(event)
        ruleset_id = pathParams.get("ruleset_id")
        content = body.get("content")
        if not ruleset_id or not content:
            raise Exps.AppException(
                "Missing ruleset_id in path param or content in request body"
            )

        # Upload ruleset
        upload_ruleset(ruleset_id, content)
        rb.set_status_code(200)
        rb.set_data(
            {"message": "Ruleset uploaded successfully", "ruleset_id": ruleset_id}
        )
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
