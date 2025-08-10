# Import from utils
from utils.constants import (
    COGNITO_APP_CLIENT_ID,
    COGNITO_USER_POOL_ID,
    DEFAULT_REGION_NAME,
)
from utils.exceptions import BadRequestException
from utils.aws_clients import get_cognito_client
from utils.helpers.other import extract_kwargs
from utils.helpers.string import is_empty
from utils.helpers.boolean import check_empty_or_throw_error


def get_user(**params):
    """Gửi yêu cầu tới Cognito để lấy thông tin của người dùng.

    Args:
        **params: Tập các tham số truyền vào, yêu cầu phải có:
            - client (boto3.Client, tùy chọn): Đối tượng client Cognito, nếu không truyền sẽ dùng client mặc định.
            - username (str): Tên đăng nhập của người dùng trong Cognito.

    Raises:
        BadRequestException: Ném lỗi nếu không có username được cung cấp.

    Returns:
        dict: Phản hồi từ Cognito chứa thông tin chi tiết của người dùng.
    """
    cognito_client = params.get("client", get_cognito_client())

    username = params.get("username", "")

    check_empty_or_throw_error(
        username, "username", "Username is required to get user's information"
    )

    response = cognito_client.admin_get_user(
        UserPoolId=COGNITO_USER_POOL_ID, Username=username
    )

    return response


def get_tokens_from_refresh_token(**params):
    """Gửi yêu cầu tới Cognito để làm mới lại Access token và Id token.

    Args:
        **params: Tập các tham số truyền vào, yêu cầu phải có:
            - client (boto3.Client, tùy chọn): Đối tượng client Cognito, nếu không truyền sẽ dùng client mặc định.
            - refresh_token (str): Mã làm mới token được cấp bởi Cognito.

    Raises:
        BadRequestException: Ném lỗi nếu không có refresh_token được cung cấp.

    Returns:
        dict: Phản hồi từ Cognito chứa Access token và Id token mới.
    """
    cognito_client = params.get("client", get_cognito_client())

    refresh_token = params.get("refresh_token", "")

    check_empty_or_throw_error(
        refresh_token, "refresh_token", "Refresh token is required to get new tokens"
    )

    response = cognito_client.get_tokens_from_refresh_token(
        RefreshToken=refresh_token, ClientId=COGNITO_APP_CLIENT_ID
    )

    return response


def initiate_auth(**params):
    """Gửi yêu cầu để đăng nhập (xác thực) một người dùng trong user pool.

    Args:
        **params: Tập các tham số truyền vào, yêu cầu phải có:
            - client (boto3.Client, tùy chọn): Đối tượng client Cognito, nếu không truyền sẽ dùng client mặc định.
            - username (str, tùy chọn): Tên đăng nhập của người dùng.
            - email (str, tùy chọn): Email của người dùng.
            - password (str): Mật khẩu của người dùng.

    Raises:
        BadRequestException: Ném lỗi nếu không có password được cung cấp.
        BadRequestException: Ném lỗi nếu không có username hoặc email.

    Returns:
        dict: Kết quả phản hồi từ Cognito sau khi xác thực người dùng.
    """
    cognito_client = params.get("client", get_cognito_client())

    username = params.get("username", "")
    email = params.get("email", "")
    password = params.get("password", "")

    check_empty_or_throw_error(
        password, "password", "Password is required to authenticate user"
    )

    if is_empty(username) and is_empty(email):
        raise BadRequestException("Username or Email is required to authenticate user")

    auth_parameters = {"PASSWORD": password}

    if email:
        auth_parameters["EMAIL"] = email
    else:
        auth_parameters["USERNAME"] = username

    response = cognito_client.initiate_auth(
        AuthFlow="USER_PASSWORD_AUTH",
        ClientId=COGNITO_APP_CLIENT_ID,
        AuthParameters=auth_parameters,
    )

    return response
