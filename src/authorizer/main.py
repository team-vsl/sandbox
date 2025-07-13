# Import built-in libraries
import os

# Import external libraries
import requests
import jwt
from jwt import InvalidTokenError
from jwcrypto import jwk

# Import from utils
from utils.constants import (
    COGNITO_APP_CLIENT_ID,
    COGNITO_USER_POOL_ID,
    DEFAULT_REGION_NAME,
)
from utils.exceptions import BadRequestException
from utils.cognito import initiate_auth

jwks_url = f"https://cognito-idp.{DEFAULT_REGION_NAME}.amazonaws.com/{COGNITO_USER_POOL_ID}/.well-known/jwks.json"


def get_authorization_token_from_headers(headers: dict) -> str:
    """Lấy token từ header Authorization trong Headers.

    Args:
        event (dict): lambda event

    Raises:
        BadRequestException: ném lỗi nếu như không tìm thấy Bearer token
        BadRequestException: ném lỗi nếu như không tìm thấy nội dung token

    Returns:
        str: token
    """
    auth_header = headers.get("Authorization") or headers.get("authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        raise BadRequestException("Missing or invalid Authorization header")

    parts = auth_header.split(" ")
    if len(parts) != 2 or not parts[1]:
        raise BadRequestException("Bearer token not found")

    return parts[1]


def get_authorization_token_from_event(event: dict) -> str:
    """Lấy token từ header Authorization trong sự kiện Lambda.

    Args:
        event (dict): lambda event

    Raises:
        BadRequestException: ném lỗi nếu như không tìm thấy Bearer token
        BadRequestException: ném lỗi nếu như không tìm thấy nội dung token

    Returns:
        str: token
    """
    headers = event.get("headers", {})
    return get_authorization_token_from_headers(headers)


def get_public_keys():
    """Lấy danh sách public keys từ Cognito JWKS endpoint.

    Returns:
        list[dict]: một list các thông tin jwk từ Cognito Pool
    """
    response = requests.get(jwks_url)
    response.raise_for_status()
    data = response.json()
    return data.get("keys", [])


def verify_token(token):
    """Xác thực token và trả về kết quả xác thực và claims (nếu thành công).

    Args:
        token (str): token

    Raises:
        ValueError: ném ra lỗi nếu như header của JWT Token là không hợp lệ
        ValueError: ném ra lỗi nếu như không tìm thấy Public Key
        ValueError: ném ra lỗi nếu như token được tạo ra không phải là từ
        Cognito Provider nguồn

    Returns:
        dict: kết quả xác thực
    """
    try:
        # Giải mã phần header để lấy kid
        decoded_header = jwt.get_unverified_header(token)
        kid = decoded_header.get("kid")
        if not kid:
            raise ValueError("Invalid token header")

        # Lấy danh sách public keys
        keys = get_public_keys()
        key_data = next((k for k in keys if k["kid"] == kid), None)
        if not key_data:
            raise ValueError("Public key not found")

        # Tạo JWK và chuyển sang PEM
        jwk_key = jwk.JWK(**key_data)
        public_key_pem = jwk_key.export_to_pem()

        # Xác thực token
        claims = jwt.decode(
            token,
            public_key_pem,
            algorithms=["RS256"],
            options={"verify_exp": True},
        )

        # Kiểm tra audience
        if claims.get("client_id") != COGNITO_APP_CLIENT_ID:
            raise ValueError("Token was not issued for this audience")

        return {
            "isAuthorized": True,
            "context": claims,
        }

    except (InvalidTokenError, ValueError) as e:
        print("❌ Token verification failed:", str(e))
        return {
            "isAuthorized": False,
        }


def sign_in(**params):
    """Đăng nhập một người dùng vào trong hệ thống với cognito

    Returns:
        dict: kết quả của đăng nhập
    """

    response = initiate_auth(**params)

    # Transform response
    auth_result = response.get("AuthenticationResult", {})

    new_response = {
        "tokenType": auth_result.get("TokenType"),
        "expiresIn": auth_result.get("ExpiresIn"),
        "accessToken": auth_result.get("AccessToken"),
        "refreshToken": auth_result.get("RefreshToken"),
        "idToken": auth_result.get("IdToken"),
    }

    return new_response
