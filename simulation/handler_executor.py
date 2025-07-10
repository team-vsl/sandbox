import asyncio
import os
import sys
import json
import traceback
import importlib.util

handlers_path = os.path.abspath(os.path.join("..", "src", "runtime", "lambda"))


def import_handler(handler_path):
    """Import a handler to execute

    Args:
        handler_path (str): path to handler

    Returns:
        Callable: handler
    """
    module_name = os.path.basename(handler_path).replace(".py", "")
    spec = importlib.util.spec_from_file_location(module_name, handler_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


async def execute_handler(handler_name: str, event: dict, context: dict):
    handler_path = os.path.abspath(os.path.join(handlers_path, f"{handler_name}.py"))

    try:
        # Import the handler module
        handler_module = import_handler(handler_path)
        handler = handler_module.handler

        # Convert body object to string if needed
        if isinstance(event.get("body"), dict):
            event["body"] = json.dumps(event["body"])

        # Call handler
        maybe_awaitable_response = handler(event, context)

        if asyncio.coroutines.iscoroutine(maybe_awaitable_response):
            response = await maybe_awaitable_response
        else:
            response = maybe_awaitable_response

        response["body"] = json.loads(response["body"])

        return response
    except Exception as e:
        print(e, traceback.format_exc(), flush=True)
        return None
