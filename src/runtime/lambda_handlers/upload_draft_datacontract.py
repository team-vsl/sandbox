# Import built-in libraries
import traceback
import os

# Import utils
import utils.exceptions as Exps
from utils.helpers import request as request_helpers
from utils.helpers.other import convert_keys_to_camel_case
from utils.logger import get_logger
from utils.response_builder import ResponseBuilder

# Import services
from services.data_contract import upload_datacontract


async def handler(event, context):
    rb = ResponseBuilder()
    logger = get_logger()

    try:
        # Extract request data
        claims = request_helpers.get_claims_from_event(event)
        path_params = request_helpers.get_path_params_from_event(event)
        body = request_helpers.get_body_from_event(event)

        response = upload_datacontract(
            {"path_params": path_params, "body": body, "meta": {"claims": claims}}
        )

        # Return response
        rb.set_status_code(200)
        rb.set_data(convert_keys_to_camel_case(response))

        return rb.create_response()

    except Exps.AppException as error:
        logger.error(f"Error | [upload_draft_datacontract]: {error}")
        return rb.create_error_response(error)

    except Exception as error:
        logger.error(
            f"Unknown error | [upload_draft_datacontract]: {error} {traceback.format_exc()}"
        )
        return rb.create_error_response(Exps.UnknownException(str(error)))

    finally:
        logger.debug("End execution of [upload_draft_datacontract]")
