import json
from typing import Any


class ErrorCodes:
    # General Errors
    Unknown = "UNKNOWN_ERROR"
    Internal = "INTERNAL_ERROR"
    NotImplemented = "NOT_IMPLEMENTED"
    Timeout = "TIMEOUT_ERROR"
    # I/O Errors
    IO = "IO_ERROR"
    FileNotFound = "FILE_NOT_FOUND"
    FileUpload = "FILE_UPLOAD_ERROR"
    FileRead = "FILE_READ_ERROR"
    FileWrite = "FILE_WRITE_ERROR"
    # Network Errors
    Network = "NETWORK_ERROR"
    ConnectionTimeout = "CONNECTION_TIMEOUT"
    HostUnreachable = "HOST_UNREACHABLE"
    # HTTP Errors
    BadRequest = "BAD_REQUEST"
    Unauthorized = "UNAUTHORIZED"
    Forbidden = "FORBIDDEN"
    NotFound = "NOT_FOUND"
    MethodNotAllowed = "METHOD_NOT_ALLOWED"
    Conflict = "CONFLICT"
    TooManyRequests = "TOO_MANY_REQUESTS"
    ServiceUnavailable = "SERVICE_UNAVAILABLE"
    # Authentication & Authorization Errors
    AuthenticationFailed = "AUTHENTICATION_FAILED"
    TokenExpired = "TOKEN_EXPIRED"
    TokenInvalid = "TOKEN_INVALID"
    PermissionDenied = "PERMISSION_DENIED"
    # Validation Errors
    Validation = "VALIDATION_ERROR"
    MissingField = "MISSING_FIELD"
    InvalidType = "INVALID_TYPE"
    OutOfRange = "OUT_OF_RANGE"
    FormatError = "FORMAT_ERROR"
    # Database Errors
    Database = "DATABASE_ERROR"
    ConnectionFailed = "DB_CONNECTION_FAILED"
    QueryFailed = "DB_QUERY_FAILED"
    TransactionFailed = "TRANSACTION_FAILED"
    # Third-Party Service Errors
    ExternalService = "EXTERNAL_SERVICE_ERROR"
    APIRequestFailed = "API_REQUEST_FAILED"
    RateLimitExceeded = "RATE_LIMIT_EXCEEDED"
    ServiceTimeout = "SERVICE_TIMEOUT"


ErrorHttpStatusMap = {
    ErrorCodes.Unknown: 500,
    ErrorCodes.Internal: 500,
    ErrorCodes.NotImplemented: 501,
    ErrorCodes.Timeout: 504,
    ErrorCodes.IO: 500,
    ErrorCodes.FileNotFound: 404,
    ErrorCodes.FileUpload: 500,
    ErrorCodes.FileRead: 500,
    ErrorCodes.FileWrite: 500,
    ErrorCodes.Network: 502,
    ErrorCodes.ConnectionTimeout: 504,
    ErrorCodes.HostUnreachable: 502,
    ErrorCodes.BadRequest: 400,
    ErrorCodes.Unauthorized: 401,
    ErrorCodes.Forbidden: 403,
    ErrorCodes.NotFound: 404,
    ErrorCodes.MethodNotAllowed: 405,
    ErrorCodes.Conflict: 409,
    ErrorCodes.TooManyRequests: 429,
    ErrorCodes.ServiceUnavailable: 503,
    ErrorCodes.AuthenticationFailed: 401,
    ErrorCodes.TokenExpired: 401,
    ErrorCodes.TokenInvalid: 401,
    ErrorCodes.PermissionDenied: 403,
    ErrorCodes.Validation: 400,
    ErrorCodes.MissingField: 400,
    ErrorCodes.InvalidType: 400,
    ErrorCodes.OutOfRange: 400,
    ErrorCodes.FormatError: 400,
    ErrorCodes.Database: 500,
    ErrorCodes.ConnectionFailed: 500,
    ErrorCodes.QueryFailed: 500,
    ErrorCodes.TransactionFailed: 500,
    ErrorCodes.ExternalService: 502,
    ErrorCodes.APIRequestFailed: 502,
    ErrorCodes.RateLimitExceeded: 429,
    ErrorCodes.ServiceTimeout: 504,
}


class AppException(Exception):
    """A base class is used to build custom exception
    in Application.

    Args:
        Exception (class): Exception class
    """

    def __init__(
        self,
        message="An unknown error occurred",
        title="Unknown Error",
        code=ErrorCodes.IO,
    ):
        super().__init__()
        self.message = message
        self.title = title
        self.code = code
        self.details = None

    @staticmethod
    def getHTTPErrorStatusCode(errorCode):
        """Get corresponding http status code by error code

        Args:
            errorCode (str): error code

        Returns:
            int: HTTP status code
        """
        httpStatusCode = ErrorHttpStatusMap[errorCode]

        if httpStatusCode is None:
            httpStatusCode = ErrorHttpStatusMap[ErrorCodes.Unknown]

        return httpStatusCode

    def setErrorDetails(self, details: list | None = []):
        """Set new details data

        Args:
            details (list, optional): various detail descriptions of error. Defaults to [].
        """
        print("Error details:", details, flush=True)
        self.details = details

    def addErrorDetail(self, detail: Any):
        """Add new detail to list

        Args:
            detail (Any): a detail description of error
        """
        if isinstance(self.details, list):
            self.details.append(detail)

    def toPlain(self):
        """Use to convert exception content to raw object (Python Dict).

        Returns:
            str: content of exception in raw object (Python Dict).
        """
        return {
            "message": self.message,
            "title": self.title,
            "code": self.code,
            "details": self.details,
        }

    def toJSON(self):
        """Use to convert exception content to JSON.

        Returns:
            str: content of exception in JSON.
        """
        return json.dumps(self.toPlain())

    def __str__(self):
        return self.message
