from http import HTTPStatus

import requests
from flask import Flask
from jose import jwt

from ..abstract.abstract_identity_loader import AbstractIdentityLoader
from ..exceptions import AuthError
from .singleton import singleton


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
        :raises AuthError: incorrect token provided.
        """
        jwks = requests.get('https://{0}/.well-known/jwks.json'.format(self.auth_domain))
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
                raise AuthError(
                    {'message': 'token_expired', 'description': 'token is expired'},
                    HTTPStatus.UNAUTHORIZED.value,
                )
            except jwt.JWTClaimsError:
                raise AuthError(
                    {'message': 'invalid_claims'},
                    HTTPStatus.UNAUTHORIZED.value,
                )
            except Exception:
                raise AuthError(
                    {'message': 'invalid_header'},
                    HTTPStatus.UNAUTHORIZED.value,
                )
            return payload['sub']

        raise AuthError(
            {'message': 'invalid_header'},
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