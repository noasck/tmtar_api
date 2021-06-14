from functools import partial, wraps
from http import HTTPStatus
from typing import Callable, List

from flask_jwt_extended import verify_jwt_in_request  # noqa: WPS319
from flask_jwt_extended import get_jwt, jwt_required  # noqa: WPS318
from flask_jwt_extended.exceptions import JWTExtendedException
from flask_restx import Namespace, abort

from ..exceptions import AuthError
from ..types import Role


def access_restriction(
    required_role: Role = Role.user,
    api: Namespace = None,
    inject_claims: bool = False,
) -> Callable:
    """
    Wrap access control decorator.

    Necessary to have claims parameter in wrapped function or method.

    :param required_role: if set, checks user role.
    :type required_role: Role
    :param api: api Namespace to create auth documentation.
    :type api: Namespace
    :param inject_claims: indicates injection of user claims into route.
    :type inject_claims: bool
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

        @api.doc(security=required_role.value)
        @jwt_required()
        @wraps(endpoint)
        def wrapper(*args, **kwargs):
            try:  # noqa: WPS229
                verify_jwt_in_request()
                claims = get_jwt()
                if required_role in {Role.root, Role.user}:
                    admin_location_id = int(claims['admin_location_id'])
            except (ValueError, TypeError, JWTExtendedException):
                # TODO: make more detailed JWTExtendedException response
                abort(HTTPStatus.FORBIDDEN.value, 'Access denied.')
            except AuthError as error:
                abort(error.status_code, error.error)

            if required_role == Role.root and admin_location_id != 1:
                abort(HTTPStatus.FORBIDDEN.value, 'Access denied.')
            if inject_claims and claims:
                wrapped_endpoint = partial(
                    endpoint,
                    claims=claims,
                )
            else:
                wrapped_endpoint = endpoint
            return wrapped_endpoint(*args, **kwargs)

        return wrapper

    return admin_required
