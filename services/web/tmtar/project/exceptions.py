class AuthError(Exception):
    """Authorization Exception."""

    def __init__(self, error, status_code):
        """
        Init Auth Exception.

        :param error: error message
        :type error: str
        :param status_code: exception http code
        :type status_code: int
        """
        self.error = error
        self.status_code = status_code
