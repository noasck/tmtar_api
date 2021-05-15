from flask import request

from ..project.exceptions import AuthError
from ..project.injector import Injector
from .model import User
from .schema import UserSchema

jwt = Injector.jwt


@jwt.user_claims_loader
def user_based_token(user: User):
    """
    Serialize single User entity data to JWT.

    :param user: User instance
    :return: serialized User Instance
    """
    return UserSchema().dump(user)


@jwt.user_identity_loader
def user_identity_lookup(user: User) -> str:
    """Define identity user field."""
    return user.identity


def get_payload():
    """Obtains the Access Token from the Authorization Header"""
    auth = request.headers.get("Authorization", None)
    if not auth:
        raise AuthError(
            {
                "code": "authorization_header_missing",
                "message": "Authorization header is expected"
            },
            401,
        )

    parts = auth.split()

    if parts[0].lower() != "bearer":
        raise AuthError(
            {
                "code": "invalid_header",
                "message": "Authorization header must start with Bearer"
            },
            401,
        )
    elif len(parts) == 1:
        raise AuthError(
            {
                "code": "invalid_header",
                "message": "Token is missing"
            },
            401,
        )
    elif len(parts) > 2:
        raise AuthError(
            {
                "code": "invalid_header",
                "message": "Authorization header is invalid"
            },
            401,
        )

    return parts[1]
