# Import from utils
from utils.constants import (
    COGNITO_APP_CLIENT_ID,
    COGNITO_USER_POOL_ID,
    DEFAULT_REGION_NAME,
)
from utils.exceptions import BadRequestException
from utils.aws_clients import get_cogito_client
from utils.helpers.other import extract_kwargs
from utils.helpers.string import is_empty


def initiate_auth(**params):
    """Gửi yêu cầu để đăng nhập (xác thực) một người dùng trong user pool

    Raises:
        BadRequestException: ném lỗi nếu như không tìm thấy password
        BadRequestException: ném lỗi nếu như không tìm thấy username hoặc email

    Returns:
        dict: kết quả của initiate_auth
    """
    cogito_client = get_cogito_client()
    username, email, password = extract_kwargs(params, "username", "email", "password")

    if is_empty(password):
        raise BadRequestException("Password is required")

    if is_empty(username) and is_empty(email):
        raise BadRequestException("Username or Email is required")

    auth_parameters = {"PASSWORD": password}

    if email:
        auth_parameters["EMAIL"] = email
    else:
        auth_parameters["USERNAME"] = username

    response = cogito_client.initiate_auth(
        AuthFlow="USER_PASSWORD_AUTH",
        ClientId=COGNITO_APP_CLIENT_ID,
        AuthParameters=auth_parameters,
    )

    return response
