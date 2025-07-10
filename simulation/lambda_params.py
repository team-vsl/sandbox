from typing import Any, Optional, Dict


def create_lambda_event(
    query: Optional[Dict[str, Any]] = {},
    params: Optional[Dict[str, Any]] = {},
    data: Optional[Any] = {},
    request_context: Optional[Dict[str, Any]] = {},
) -> Dict[str, Any]:
    return {
        "queryStringParameters": query,
        "pathParameters": params,
        "headers": {
            "Content-Type": "application/json",
            "Authorization": "Bearer test-token",
        },
        "body": data,
        "requestContext": request_context,
    }


def add_claims_to_request_ctx(request_ctx: dict, claims: dict):
    """Add custom claims to request_ctx

    Args:
        claims (dict): claims from JWT Token

    Returns:
        dict: request context with claims
    """
    authorizer = {"lambda": claims}
    request_ctx["authorizer"] = authorizer

    return request_ctx
