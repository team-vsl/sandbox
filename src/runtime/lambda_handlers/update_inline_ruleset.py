# Import built-in libraries
import traceback

# Import 3rd-party libraries

# Import utils
import utils.exceptions as Exps
from utils.helpers import request as request_helpers
from utils.logger import get_logger
from utils.response_builder import ResponseBuilder

from utils.glue import update_inline_ruleset_in_job


def handler(event, context):
    rb = ResponseBuilder()
    logger = get_logger()

    try:
        # Extract request data
        claims = request_helpers.get_claims_from_event(event)
        path_params = request_helpers.get_path_params_from_event(event)
        body = request_helpers.get_body_from_event(event)

        response = update_inline_ruleset_in_job(
            job_name=path_params.get("job_name"),
            new_ruleset=body.get("content"),
            dq_node_name="Evaluate Data Quality",
        )

        # Return response
        rb.set_status_code(200)
        rb.set_data({"jobName": response})

        return rb.create_response()
    except Exps.AppException as error:
        logger.error(f"Error | [update_inline_ruleset]: {error}")
        return rb.create_error_response(error)
    except Exception as error:
        logger.error(
            f"Uknown error | [update_inline_ruleset]: {error} {traceback.format_exc()}"
        )
        return rb.create_error_response(Exps.UnknownException(str(error)))
    finally:
        logger.debug("End execution of [update_inline_ruleset]")
