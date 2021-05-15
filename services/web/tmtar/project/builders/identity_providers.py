import json
from urllib.request import urlopen

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

    @singleton("verify_token")
    def verify_identity(self, token) -> str:
        """
        Verify Auth0 access_token.
        :param token: Auth0 access_token.
        :type token: str.
        :return:
        :rtype:
        """
        json_url = urlopen("https://" + self.auth_domain + "/.well-known/jwks.json")
        jwks = json.loads(json_url.read())
        unverified_header = jwt.get_unverified_header(token)
        rsa_key = {}
        for key in jwks["keys"]:
            if key["kid"] == unverified_header["kid"]:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"]
                }
        if rsa_key:
            try:
                payload = jwt.decode(
                    token,
                    rsa_key,
                    algorithms=self.algorithm,
                    audience=self.api_audience,
                    issuer="https://" + self.auth_domain + "/",
                )
            except jwt.ExpiredSignatureError:
                raise AuthError(
                    {'message': 'token_expired', 'description': 'token is expired'},
                    401,
                )
            except jwt.JWTClaimsError:
                raise AuthError(
                    {"message": "invalid_claims"},
                    401,
                )
            except Exception:
                raise AuthError(
                    {"message": "invalid_header"},
                    401,
                )
            return payload['sub']

        raise AuthError(
            {"message": "invalid_header"},
            401,
        )


class TestIdentityLoader(AbstractIdentityLoader):
    """Class responsible for user identity in testing environment."""

    def __init__(self, app: Flask):
        app.logger.warning("Test Identity Loader is in use!")

    def verify_identity(self, token) -> str:
        """
        Mock auth.

        :param token: identity
        :return: identity
        """
        return token.strip()
