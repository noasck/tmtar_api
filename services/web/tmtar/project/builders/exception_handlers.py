from functools import wraps

from flask_restx import abort


def wrap_exception(
    endpoint,
    status: int = 500,
    message: str = 'Unknown error.',
    exception: type = Exception,
):
    """
    Wrap route to handle exceptions.

    :param endpoint: route endpoint.
    :type endpoint: Callable
    :param status: http status
    :type status: int
    :param message: response message.
    :type message: str
    :param exception: Exception class to handle.
    :type exception: type
    :return: wrapper
    :rtype: Callable
    """
    @wraps(endpoint)
    def wrapper(*args, **kwargs):
        try:
            return endpoint(*args, **kwargs)
        except exception:
            return abort(status, message)

    return wrapper
