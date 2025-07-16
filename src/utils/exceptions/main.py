from .base import AppException, ErrorCodes


class UnknownException(AppException):
    """Thrown when an unexpected and unknown event occurred"""

    def __init__(self, message="An unknow error occured", title="Unknown Error"):
        super().__init__(message, title)


class IOException(AppException):
    """Thrown when a unexpected IO event occurred"""

    def __init__(self, message="An IO error occurred", title="IO Error"):
        super().__init__(message, title, ErrorCodes.IO)


class InternalException(AppException):
    """Thrown when an unexpected internal event occurred."""

    def __init__(self, message="An internal error occurred.", title="Internal Error"):
        super().__init__(message, title, ErrorCodes.Internal)


class NotImplementedException(AppException):
    """Thrown when an event isn't implemented."""

    def __init__(
        self, message="This feature is not implemented.", title="Not Implemented"
    ):
        super().__init__(message, title, ErrorCodes.NotImplemented)


class TimeoutException(AppException):
    """Thrown when a timeout is reached."""

    def __init__(self, message="The operation timed out.", title="Timeout"):
        super().__init__(message, title, ErrorCodes.Timeout)


class FileNotFoundException(AppException):
    """Thrown when a file isn't found."""

    def __init__(self, message="File not found.", title="File Not Found"):
        super().__init__(message, title, ErrorCodes.FileNotFound)


class FileUploadException(AppException):
    """Thrown when an unexpected file upload event occurred."""

    def __init__(self, message="File upload failed.", title="File Upload Error"):
        super().__init__(message, title, ErrorCodes.FileUpload)


class FileReadException(AppException):
    """Thrown when an unexpected file read event occurred."""

    def __init__(self, message="Failed to read file.", title="File Read Error"):
        super().__init__(message, title, ErrorCodes.FileRead)


class FileWriteException(AppException):
    """Thrown when an unexpected file write event occurred."""

    def __init__(self, message="Failed to write file.", title="File Write Error"):
        super().__init__(message, title, ErrorCodes.FileWrite)


class NetworkException(AppException):
    """Thrown when a network problem occurs."""

    def __init__(self, message="Network error occurred.", title="Network Error"):
        super().__init__(message, title, ErrorCodes.Network)


class ConnectionTimeoutException(AppException):
    """Thrown when a connection times out."""

    def __init__(self, message="Connection timed out.", title="Connection Timeout"):
        super().__init__(message, title, ErrorCodes.ConnectionTimeout)


class HostUnreachableException(AppException):
    """Thrown when a requested host is unreachable."""

    def __init__(self, message="Host is unreachable.", title="Host Unreachable"):
        super().__init__(message, title, ErrorCodes.HostUnreachable)


class BadRequestException(AppException):
    """Thrown when a request is bad."""

    def __init__(self, message="Bad request.", title="Bad Request"):
        super().__init__(message, title, ErrorCodes.BadRequest)


class UnauthorizedException(AppException):
    """Thrown when a request is unauthorized."""

    def __init__(self, message="Unauthorized access.", title="Unauthorized"):
        super().__init__(message, title, ErrorCodes.Unauthorized)


class ForbiddenException(AppException):
    """Thrown when a request is forbidden."""

    def __init__(self, message="Access is forbidden.", title="Forbidden"):
        super().__init__(message, title, ErrorCodes.Forbidden)


class NotFoundException(AppException):
    """Thrown when a requested resource is not found."""

    def __init__(self, message="Resource not found.", title="Not Found"):
        super().__init__(message, title, ErrorCodes.NotFound)


class MethodNotAllowedException(AppException):
    """Thrown when an HTTP method is not allowed for the requested resource."""

    def __init__(
        self, message="The HTTP method is not allowed.", title="Method Not Allowed"
    ):
        super().__init__(message, title, ErrorCodes.MethodNotAllowed)


class ConflictException(AppException):
    """Thrown when a conflict occurs due to a resource state mismatch."""

    def __init__(self, message="A conflict occurred.", title="Conflict"):
        super().__init__(message, title, ErrorCodes.Conflict)


class TooManyRequestsException(AppException):
    """Thrown when too many requests are made in a short period of time."""

    def __init__(self, message="Too many requests.", title="Too Many Requests"):
        super().__init__(message, title, ErrorCodes.TooManyRequests)


class ServiceUnavailableException(AppException):
    """Thrown when the service is temporarily unavailable."""

    def __init__(
        self, message="Service is temporarily unavailable.", title="Service Unavailable"
    ):
        super().__init__(message, title, ErrorCodes.ServiceUnavailable)


class AuthenticationFailedException(AppException):
    """Thrown when authentication fails due to invalid credentials."""

    def __init__(self, message="Authentication failed.", title="Authentication Failed"):
        super().__init__(message, title, ErrorCodes.AuthenticationFailed)


class TokenExpiredException(AppException):
    """Thrown when a token has expired."""

    def __init__(self, message="Token has expired.", title="Token Expired"):
        super().__init__(message, title, ErrorCodes.TokenExpired)


class TokenInvalidException(AppException):
    """Thrown when a token is invalid."""

    def __init__(self, message="Token is invalid.", title="Invalid Token"):
        super().__init__(message, title, ErrorCodes.TokenInvalid)


class PermissionDeniedException(AppException):
    """Thrown when access is denied due to insufficient permissions."""

    def __init__(self, message="Permission denied.", title="Permission Denied"):
        super().__init__(message, title, ErrorCodes.PermissionDenied)


class ValidationException(AppException):
    """Thrown when validation of input data fails."""

    def __init__(self, message="Validation failed.", title="Validation Error"):
        super().__init__(message, title, ErrorCodes.Validation)


class MissingFieldException(AppException):
    """Thrown when a required field is missing."""

    def __init__(self, message="A required field is missing.", title="Missing Field"):
        super().__init__(message, title, ErrorCodes.MissingField)


class InvalidTypeException(AppException):
    """Thrown when a value has an invalid type."""

    def __init__(self, message="Invalid type provided.", title="Invalid Type"):
        super().__init__(message, title, ErrorCodes.InvalidType)


class OutOfRangeException(AppException):
    """Thrown when a value is outside the allowed range."""

    def __init__(self, message="Value is out of range.", title="Out of Range"):
        super().__init__(message, title, ErrorCodes.OutOfRange)


class FormatErrorException(AppException):
    """Thrown when a value has an incorrect format."""

    def __init__(self, message="Incorrect format.", title="Format Error"):
        super().__init__(message, title, ErrorCodes.FormatError)


class DatabaseException(AppException):
    """Thrown when a database error occurs."""

    def __init__(self, message="Database error occurred.", title="Database Error"):
        super().__init__(message, title, ErrorCodes.Database)


class ConnectionFailedException(AppException):
    """Thrown when a connection to a service or database fails."""

    def __init__(self, message="Failed to connect.", title="Connection Failed"):
        super().__init__(message, title, ErrorCodes.ConnectionFailed)


class QueryFailedException(AppException):
    """Thrown when a database query fails."""

    def __init__(self, message="Query execution failed.", title="Query Failed"):
        super().__init__(message, title, ErrorCodes.QueryFailed)


class TransactionFailedException(AppException):
    """Thrown when a database transaction fails."""

    def __init__(self, message="Transaction failed.", title="Transaction Failed"):
        super().__init__(message, title, ErrorCodes.TransactionFailed)


class ExternalServiceException(AppException):
    """Thrown when an external service returns an error."""

    def __init__(
        self, message="External service error.", title="External Service Error"
    ):
        super().__init__(message, title, ErrorCodes.ExternalService)


class APIRequestFailedException(AppException):
    """Thrown when an API request fails."""

    def __init__(self, message="API request failed.", title="API Request Failed"):
        super().__init__(message, title, ErrorCodes.APIRequestFailed)


class RateLimitExceededException(AppException):
    """Thrown when a rate limit is exceeded."""

    def __init__(self, message="Rate limit exceeded.", title="Rate Limit Exceeded"):
        super().__init__(message, title, ErrorCodes.RateLimitExceeded)


class ServiceTimeoutException(AppException):
    """Thrown when a service request times out."""

    def __init__(self, message="Service request timed out.", title="Service Timeout"):
        super().__init__(message, title, ErrorCodes.ServiceTimeout)
