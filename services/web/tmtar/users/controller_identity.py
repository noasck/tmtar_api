from http import HTTPStatus

from flask import request
from flask_jwt_extended import create_access_token

from ..project.exceptions import AuthError
from ..project.injector import Injector
from .model import User
from .schema import UserSchema

jwt = Injector.jwt


def create_internal_jwt(user: User):
    """Create API internal JWT access token."""
    user_dumped = UserSchema().dump(user)
    return create_access_token(user.identity, additional_claims=user_dumped)


def get_payload():
    """Obtain the Access Token from the Authorization Header."""
    auth = request.headers.get('Authorization', None)
    if not auth:
        raise AuthError(
            {
                'code': 'authorization_header_missing',
                'message': 'Authorization header is expected',
            },
            HTTPStatus.UNAUTHORIZED.value,
        )

    parts = auth.split()

    if len(parts) == 1:
        raise AuthError(
            {
                'code': 'invalid_header',
                'message': 'Token is missing',
            },
            HTTPStatus.UNAUTHORIZED.value,
        )
    elif parts[0].lower() != 'bearer' or len(parts) > 2:
        raise AuthError(
            {
                'code': 'invalid_header',
                'message': 'Authorization header is invalid',
            },
            HTTPStatus.UNAUTHORIZED.value,
        )

    return parts[1]
