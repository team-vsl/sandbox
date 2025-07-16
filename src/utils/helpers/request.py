import json


def get_body_from_event(event: dict) -> dict:
    """Get the body from the event. If the body is a string, parse it as JSON.

    Args:
        event (dict): event from AWS Lambda

    Returns:
        dict: content of body
    """
    body = event.get("body", {})
    if isinstance(body, str):
        body = json.loads(body)
    return body


def get_path_params_from_event(event: dict) -> dict:
    """Get the path parameters from the event

    Args:
        event (dict): event from AWS Lambda

    Returns:
        dict: path parameters
    """
    pathParameters = event.get("pathParameters", {})
    return pathParameters


def getQueryFromEvent(event: dict) -> dict:
    """Get the query string from the event

    Args:
        event (dict): event from AWS Lambda

    Returns:
        dict: query string parameters
    """
    queryStringParameters = event.get("queryStringParameters", {})
    return queryStringParameters


def getHeadersFromEvent(event: dict):
    """
    Get the headers from the event.
    """
    headers = event.get("headers", {})
    return headers


def get_claims_from_event(event: dict):
    """Get claims from the event.

    Args:
        event (dict): event from AWS Lambda

    Returns:
        dict: JWT claims
    """
    requestContext = event.get("requestContext", None)

    if requestContext is None:
        return

    authorizer = requestContext.get("authorizer")

    if authorizer is None:
        return

    return authorizer.get("lambda", {})
