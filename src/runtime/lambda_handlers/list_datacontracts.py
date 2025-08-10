# Import built-in libraries
import traceback

# Import 3rd-party libraries

# Import utils
import utils.exceptions as Exps
from utils.helpers import request as request_helpers
from utils.logger import get_logger
from utils.response_builder import ResponseBuilder

from services.data_contract import list_datacontracts


async def handler(event, context):
    rb = ResponseBuilder()
    logger = get_logger()

    try:
        # Extract request data
        claims = request_helpers.get_claims_from_event(event)
        path_params = request_helpers.get_path_params_from_event(event)
        query = request_helpers.get_query_from_event(event)
        body = request_helpers.get_body_from_event(event)

        response = list_datacontracts({"path_params": path_params, "query": query})

        # Return response
        rb.set_status_code(200)
        rb.set_data(response)

        return rb.create_response()
    except Exps.AppException as error:
        logger.error(f"Error | [list_datacontracts]: {error}")
        return rb.create_error_response(error)
    except Exception as error:
        logger.error(
            f"Uknown error | [list_datacontracts]: {error} {traceback.format_exc()}"
        )
        return rb.create_error_response(Exps.UnknownException(str(error)))
    finally:
        logger.debug("End execution of [list_datacontracts]")
