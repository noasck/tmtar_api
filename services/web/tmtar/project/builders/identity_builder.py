from http import HTTPStatus

import requests
from flask import Flask
from jose import jwt

from ..abstract.abstract_identity_loader import AbstractIdentityLoader
from ..decorators.singleton import singleton
from ..exceptions import AuthError


class ProductionIdentityLoader(AbstractIdentityLoader):
    """Class responsible for user identity validation in production."""

    def __init__(self, app: Flask):
        """Get constants for token verification from Flask app config."""
        self.auth_domain = app.config.get('AUTH0_DOMAIN')
        self.algorithm = app.config.get('ALGORITHMS')
        self.api_audience = app.config.get('API_AUDIENCE')

    @singleton('verify_token')
    def verify_identity(self, token) -> str:
        """
        Verify Auth0 access_token.

        :param token: Auth0 access_token.
        :type token: str.
        :return: payload sub.
        :rtype: str
        :raise AuthError: incorrect token provided.
        """
        jwks = requests.get('https://{0}/.well-known/jwks.json'.format(self.auth_domain)).json()
        unverified_header = jwt.get_unverified_header(token)
        rsa_key = {}
        for key in jwks['keys']:
            if key['kid'] == unverified_header['kid']:
                rsa_key = {
                    'kty': key['kty'],
                    'kid': key['kid'],
                    'use': key['use'],
                    'n': key['n'],
                    'e': key['e'],
                }
        if rsa_key:
            try:
                payload = jwt.decode(
                    token,
                    rsa_key,
                    algorithms=self.algorithm,
                    audience=self.api_audience,
                    issuer='https://{0}/'.format(self.auth_domain),
                )
            except jwt.ExpiredSignatureError:
                self.raise_exception('token is expired')
            except jwt.JWTClaimsError:
                self.raise_exception('invalid claims')
            except Exception:
                self.raise_exception('invalid header')

            return payload['sub']

        self.raise_exception('invalid header')

    @classmethod
    def raise_exception(cls, message: str) -> None:
        """
        Raise Auth Exception with UNAUTHORIZED code.

        :param message: message to inform user.
        :type message: str
        :raises AuthError: incorrect token provided.
        """
        raise AuthError(
            message,
            HTTPStatus.UNAUTHORIZED.value,
        )


class TestIdentityLoader(AbstractIdentityLoader):
    """Class responsible for user identity in testing environment."""

    def __init__(self, app: Flask):
        """
        Init Test identity provider.

        :param app: main Flask app instance.
        :type app: Flask
        """
        app.logger.warning('Test Identity Loader is in use!')

    def verify_identity(self, token) -> str:
        """
        Mock auth.

        :param token: identity
        :return: identity
        """
        return token.strip()
