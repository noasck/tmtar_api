from functools import wraps
from http import HTTPStatus
from typing import Callable

from flask_jwt_extended import verify_jwt_in_request  # noqa: WPS319
from flask_jwt_extended import get_jwt_claims, jwt_required  # noqa: WPS318
from flask_jwt_extended.exceptions import JWTExtendedException
from flask_restx import Namespace, abort


def access_restriction(
    root_required: bool = False,
    api: Namespace = None,
) -> Callable:
    """
    Wrap access control decorator.

    :param root_required: if set, checks admin_location_id to be 0.
    :type root_required: bool
    :param api: api Namespace to create auth documentation.
    :type api: Namespace
    :return: secured endpoint wrapper.
    :rtype: Callable
    """

    def admin_required(endpoint):
        """
        Protect endpoint with jwt claims. Extract user role.

        :param endpoint: route endpoint.
        :type endpoint: Callable
        :return: wrapped function.
        :rtype: Callable
        """

        @api.doc(security='root' if root_required else 'admin')
        @jwt_required
        @wraps(endpoint)
        def wrapper(*args, **kwargs):
            try:  # noqa: WPS229
                verify_jwt_in_request()
                claims = get_jwt_claims()
                admin_location_id = int(claims['admin_location_id'])
            except (ValueError, TypeError, JWTExtendedException):
                # TODO: make more detailed JWTExtendedException response
                return abort(HTTPStatus.FORBIDDEN.value, 'Access denied.')
            if root_required and admin_location_id != 1:
                return abort(HTTPStatus.FORBIDDEN.value, 'Access denied.')
            return endpoint(*args, **kwargs)

        return wrapper

    return admin_required
