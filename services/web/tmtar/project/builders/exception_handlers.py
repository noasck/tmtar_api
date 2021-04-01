from flask_restx import abort
from functools import wraps


def wrap_exception(endpoint, status: int = 500, message: str = "Unknown error.", exception: type = Exception):
    @wraps(endpoint)
    def wrapper(*args, **kwargs):
        try:
            return endpoint(*args, **kwargs)
        except exception:
            return abort(status, message)
    return wrapper
