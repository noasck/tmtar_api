from flask import Flask
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy

from .database_loader import DatabaseSetup
from .identity_providers import ProductionIdentityLoader, TestIdentityLoader
from .singleton import singleton


class ModulesSetup(object):
    """Setups all app modules."""

    _authorizations = {
        'admin': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
        },
        'root': {
            'type': 'apiKey',
            'in': 'header',

            'name': 'Authorization',
        },
        'loggedIn': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
        },
        'auth0_login': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
        },
    }

    @classmethod
    @singleton('jwt')
    def configure_jwt(cls, app: Flask) -> JWTManager:
        """Configure JSON web token plugin."""
        return JWTManager(app)

    @classmethod
    @singleton('db')
    def configure_db(cls, app: Flask) -> SQLAlchemy:
        """Configure SQLAlchemy ORM plugin."""
        return SQLAlchemy(app)

    @classmethod
    def initialize_db(cls, app: Flask, db: SQLAlchemy):
        """Instantiate database tables and seed necessary data."""
        if app.config['FLASK_ENV'] in {'development', 'testing'}:
            DatabaseSetup.tear_down_db(app, db)
            DatabaseSetup.set_up_db(app, db)
            DatabaseSetup.seed_db(app, db)

    @classmethod
    @singleton('ma')
    def configure_ma(cls, app: Flask) -> Marshmallow:
        """Configure Marshmallow plugin."""
        return Marshmallow(app)

    @classmethod
    @singleton('api')
    def configure_api(cls, app: Flask) -> Api:
        """Configure Flask RestX plugin."""
        doc = '/'
        if app.config['FLASK_ENV'] == 'production':
            doc = False

        return Api(
            app,
            app.config['API_TITLE'],
            doc=doc,
            authorizations=cls._authorizations,
        )

    @classmethod
    def configure_health_route(cls, app: Flask):
        """
        Add /health route to check server status.

        :param app: main Flask app.
        """
        @app.route('/api/health', methods=['GET'])
        def health():
            return 'Healthy'

    @classmethod
    def configure_identity(cls, app: Flask):
        """Configure identity provider."""
        if app.config.get('FLASK_ENV') == 'production':
            provider = ProductionIdentityLoader(app)
        else:
            provider = TestIdentityLoader(app)

        return provider.get_verifier()

    @classmethod
    def configure_cli(cls, app: Flask, db: SQLAlchemy):
        """
        Register CLI commands for db manipulation.

        :param app: main Flask app.
        :type app: Flask
        :param db: db connection instance.
        :type db: SQLAlchemy
        """

        @app.cli.command('set_up')
        def set_up():
            """Create all ab tables and seed values."""
            DatabaseSetup.set_up_db(app, db)
            DatabaseSetup.seed_db(app, db)

        @app.cli.command('tear_down')
        def tear_down():
            """Drop all ab tables."""
            DatabaseSetup.tear_down_db(app, db)
