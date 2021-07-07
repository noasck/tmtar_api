from abc import ABC
from http import HTTPStatus


class InternalAPIException(ABC, Exception):
    """Internal API Error Base class."""

    def __init__(self, error, status_code):
        """
        Init API Exception.

        :param error: error message
        :type error: str
        :param status_code: exception http code
        :type status_code: int
        """
        self.error = error
        self.status_code = status_code


class AuthError(InternalAPIException):
    """Authorization Exception."""


class LocationAccessError(InternalAPIException):
    """Exception during accessing."""

    def __init__(self):
        """Instantiate API Exception."""
        super().__init__(
            "You don't have permissions to access this location!",
            HTTPStatus.FORBIDDEN,
        )
