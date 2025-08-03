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


def get_user(**params):
    """Gửi yêu cầu tới Cognito để lấy thông tin của người dùng

    Raises:
        BadRequestException: ném lỗi nếu như không có username

    Returns:
        dict: phản hồi từ cognito
    """
    cognito_client = get_cognito_client()
    tpl = extract_kwargs(params, "username")
    username = tpl[0]

    if is_empty(username):
        raise BadRequestException("Username is required to get user's information")

    response = cognito_client.admin_get_user(
        UserPoolId=COGNITO_USER_POOL_ID, Username=username
    )

    return response

def get_tokens_from_refresh_token(**params):
    """Gửi yêu cầu tới Cognito để làm mới lại Access và Id token

    Returns:
        dict: phản hồi từ cognito
    """
    cognito_client = get_cognito_client()
    r = extract_kwargs(params, "refresh_token")
    
    refresh_token = r[0]
    
    if is_empty(refresh_token):
        raise BadRequestException("Refresh token is required to get new access, id token")
    
    response = cognito_client.get_tokens_from_refresh_token(
        RefreshToken=refresh_token, 
        ClientId=COGNITO_APP_CLIENT_ID
    )
    
    return response

def initiate_auth(**params):
    """Gửi yêu cầu để đăng nhập (xác thực) một người dùng trong user pool

    Raises:
        BadRequestException: ném lỗi nếu như không tìm thấy password
        BadRequestException: ném lỗi nếu như không tìm thấy username hoặc email

    Returns:
        dict: kết quả của initiate_auth
    """
    cognito_client = get_cognito_client()
    username, email, password = extract_kwargs(params, "username", "email", "password")

    if is_empty(password):
        raise BadRequestException("Password is required to sign in")

    if is_empty(username) and is_empty(email):
        raise BadRequestException("Username or Email is required to sign in")

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
