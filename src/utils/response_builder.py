import json

from .exceptions import (
    ErrorHttpStatusMap,
    InternalException,
    IOException,
    InvalidTypeException,
)


_DEFAULT_HEADERS = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
}


class ResponseBuilder:
    """A class is used to create response builder
    to create response for client
    """

    def __init__(self, statusCode=200, data=None, headers=_DEFAULT_HEADERS):
        self.statusCode = statusCode
        self.data = data
        self.headers = headers
        self.meta = None
        pass

    @staticmethod
    def checkStatusCodeType(statusCode, options: dict | None = None):
        """Check type of status code

        Args:
            statusCode (int | str): value of status code
            options (dict): options of this method

        Raises:
            IOException: If statusCode is empty and options.canThrowError is True
            IOException: If statusCode isn't int or str and options.canThrowError is True

        Returns:
            bool: if statusCode has correct type or not
        """
        # Options is an object which contains some
        # information to tell this method how to execute,
        # including these information:
        #   - `canThrowError`: if this method checks fail, it will throw error
        #   instead of returning boolean.
        if statusCode is None:
            if options and options.get("canThrowError"):
                raise IOException("StatusCode cannot be empty")
            return False

        if type(statusCode) is not int and type(statusCode) is not str:
            if options and options.get("canThrowError"):
                raise IOException("StatusCode must be a number or string")
            return False

        return True

    def setStatusCode(self, statusCode):
        """Use to set status code for response

        Args:
            statusCode (int | str): value of status code which you want to set
        """
        # Check type of status code first
        ResponseBuilder.checkStatusCodeType(statusCode, {"canThrowError": True})
        self.statusCode = statusCode

    def setData(self, data: int | str | dict):
        """Use to set data for response

        Args:
            data (int | str | dict): data for response body
        """
        self.data = data

    def setHeaders(self, headers: dict):
        """Use to set headers for response

        Args:
            headers (dict): headers of http response

        Raises:
            InvalidTypeException: if headers is not a dict
        """
        if type(headers) is not dict:
            raise InvalidTypeException("headers must be a dict")

        self.headers = headers

    def setMetadata(self, meta: dict):
        """Set metadata for response

        Args:
            meta (dict): metadata of response

        Raises:
            InvalidTypeException: if headers is not a dict
        """
        if type(meta) is not dict:
            raise InvalidTypeException("meta must be a dict")

        self.meta = meta

    def createErrorBody(self, error: Exception):
        """Create a body for error response

        Args:
            error (Exception): error is raised from execution

        Raises:
            IOException: if error is None (empty)
            InvalidTypeException: if error isn't created from a valid exception class

        Returns:
            dict: a body for error response
        """
        if error is None:
            raise IOException("Error cannot be empty")

        # If error doesn't have `title` or `code` (custom properties),
        # it meant the error is a instance of language Exception.
        # So I need to be convert to standard Exception.
        if not hasattr(error, "title") or not hasattr(error, "code"):
            # Internal Server Error can be considered as
            # Unknown Error / Exception
            error = InternalException(str(error))

        return json.dumps(
            {"error": error.toPlain(), "data": self.data, "meta": self.meta}
        )

    def createBody(self):
        """Create a body for response

        Returns:
            dict: a body for error response
        """
        return json.dumps({"data": self.data, "meta": self.meta})

    def createErrorResponse(self, error: Exception, statusCode: str | None = None):
        """Create an error response

        Args:
            error (Exception): error is raised from execution
            statusCode (str | None): value of status code

        Returns:
            dict: an error response
        """
        body = self.createErrorBody(error)

        self.statusCode = ErrorHttpStatusMap[error.code]

        # Override value if `statusCode` is set
        if ResponseBuilder.checkStatusCodeType(statusCode):
            self.statusCode = statusCode

        return {"statusCode": self.statusCode, "headers": self.headers, "body": body}

    def createResponse(self, statusCode: str | None = None):
        """Create a response

        Returns:
            dict: a response
        """
        if (statusCode is not None) or (
            statusCode is not None and self.statusCode is None
        ):
            self.setStatusCode(statusCode)

        body = self.createBody()

        return {"statusCode": self.statusCode, "headers": self.headers, "body": body}
