class AuthError(Exception):
    """Authorization Exception."""
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code
