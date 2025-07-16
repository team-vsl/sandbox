from fastapi.responses import JSONResponse


def json_response(lambda_response: dict):
    """Generate fastapi response from lambda response

    Args:
        lambda_response (dict): response object from lambda

    Returns:
        JSONResponse: json response from fastapi
    """
    return JSONResponse(
        content=lambda_response.get("body"),
        status_code=lambda_response.get("statusCode"),
        headers=lambda_response.get("headers"),
    )
