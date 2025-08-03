import traceback
import utils.exceptions as Exps
from utils.helpers import request as request_helpers
from utils.logger import get_logger
from utils.response_builder import ResponseBuilder

# Import DataModelAgent
from genai.sub_agent.data_model import DataModelAgent


# Mock LLM instance (bạn cần thay thế bằng LLM thực tế khi triển khai)
class DummyLLM:
    def invoke(self, messages):
        # Trả về kết quả mẫu để test flow
        return type(
            "obj",
            (object,),
            {"content": '{"type": "table", "description": "Sample", "fields": {}}'},
        )()


async def handler(event, context):
    rb = ResponseBuilder()
    logger = get_logger()
    try:
        body = request_helpers.get_body_from_event(event)
        user_input = body.get("input")
        if not user_input:
            raise Exps.AppException("Missing 'input' in request body")

        # Khởi tạo agent với DummyLLM
        agent = DataModelAgent(DummyLLM())
        result = agent.invoke(user_input)
        rb.set_status_code(200)
        rb.set_data(result)
        return rb.create_response()
    except Exps.AppException as error:
        logger.error(f"Error | [invoke_agent]: {error}")
        return rb.create_error_response(error)
    except Exps.InternalException as error:
        error.message = (
            "There is an internal error in server Contact with Admin to get support."
        )
        logger.error(f"Error | [invoke_agent]: {error}")
        return rb.create_error_response(error)
    except Exception as error:
        logger.error(f"Uknown error | [invoke_agent]: {error} {traceback.format_exc()}")
        error.message = (
            "There is an internal error in server Contact with Admin to get support."
        )
        return rb.create_error_response(Exps.UnknownException(str(error)))
    finally:
        logger.debug("End execution of [invoke_agent]")
