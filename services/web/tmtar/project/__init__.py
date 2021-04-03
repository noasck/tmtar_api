from flask import Flask
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from werkzeug.middleware.proxy_fix import ProxyFix

from ..routes import register_routes
from .helpers.cors_headers import register_cors
from .helpers.ext_loader import ModulesSetupLoader as MLoader
from .injector import Injector


class AppModule(object):
    """Class providing application initialization."""

    def __init__(self):
        """App module initialized with app config and Flask instance."""
        try:
            self.app = Injector.app
        except AttributeError:
            config = 'tmtar.project.config.Config'
            app = Flask(__name__)
            app.config.from_object(config)
            app.logger.info('Application created successfully!')
            self.app = app

    def configure(self):
        """Configure main modules and extensions."""
        try:
            Injector.configured is True  # noqa: B015,WPS428
        except (AssertionError, AttributeError):
            self.app.wsgi_app = ProxyFix(self.app.wsgi_app)

            # Extensions modules
            jwt: JWTManager = MLoader.configure_jwt(self.app)
            db: SQLAlchemy = MLoader.configure_db(self.app)
            api: Api = MLoader.configure_api(self.app)
            ma: Marshmallow = MLoader.configure_ma(self.app)

            Injector.inject(db, to='db')
            Injector.inject(jwt, to='jwt')
            Injector.inject(ma, to='ma')
            Injector.inject(api, to='api')
            Injector.inject(self.app, to='app')

            # DB tables initialization
            MLoader.tables_db_init(self.app, db)

            # Adding /health route
            MLoader.configure_health_route(self.app)

            # Registering all modules
            register_routes(api=api)

            # Adding CORS policy
            register_cors(self.app)

            self.app.logger.info('Application initialization finished!')

            Injector.inject(instance=True, to='configured')

        return self.app
