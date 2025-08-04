# Import built-in libraries
import json

# Import external libraries
from fastapi.responses import JSONResponse
from fastapi import Request, HTTPException, Depends
from starlette.middleware.base import BaseHTTPMiddleware

# Import from authorizer
from authorizer import verify_token, get_authorization_token_from_headers

# Import utils
import utils.exceptions as Exps
from utils.response_builder import ResponseBuilder
from fastapi_response import json_response


class AuthorizationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        token = get_authorization_token_from_headers(request.headers)
        result = verify_token(token)

        if result.get("isAuthorized") == False:
            rb = ResponseBuilder()
            err = Exps.UnauthorizedException()
            response = rb.create_error_response(err)

            return json_response(response)

        request.state.claims = result.get("context")

        return await call_next(request)


def authorization_dependency(required_role: str = None):
    async def wrapper(request: Request):
        rb = ResponseBuilder()
        try:
            token = get_authorization_token_from_headers(request.headers)
            result = verify_token(token)

            if not result.get("isAuthorized"):
                raise Exps.UnauthorizedException("Cannot access to this route")

            claims = result.get("context")
            role = claims.get("role") or claims.get("custom:role")

            # Nếu cần kiểm tra vai trò:
            if required_role and role != required_role:
                raise HTTPException(status_code=403, detail="Forbidden")

            return claims
        except Exps.AppException as err:
            response = rb.create_error_response(err)
            response["body"] = json.loads(response["body"])
            raise HTTPException(
                status_code=response["statusCode"],
                detail=response["body"],
                headers=response.get("headers"),
            )
        except Exception as err:
            response = rb.create_error_response(Exps.InternalException(str(err)))
            raise HTTPException(
                status_code=response["statusCode"],
                detail=response["body"],
                headers=response.get("headers"),
            )

    return Depends(wrapper)
