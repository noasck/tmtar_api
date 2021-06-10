from flask import Flask
from flask_cors import CORS
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from werkzeug.middleware.proxy_fix import ProxyFix

from ..routes import register_routes
from .builders.extension_loader import ModulesSetup as MLoader
from .injector import Injector

# TODO: remove logic from __init__ everywhere. It's a bad style.


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
            app.wsgi_app = ProxyFix(app.wsgi_app)

            self.app = app
            Injector.inject(self.app, to='app')

            self._configure_plugins()

    def _configure_plugins(self):
        """Configure main modules and extensions."""
        # Extensions modules
        MLoader.configure_jwt(self.app)
        # Inject auth provider
        MLoader.configure_identity(self.app)

        db: SQLAlchemy = MLoader.configure_db(self.app)
        api: Api = MLoader.configure_api(self.app)
        MLoader.configure_ma(self.app)

        # Adding /health route
        MLoader.configure_health_route(self.app)

        # Registering all modules
        register_routes(api=api)

        # Adding CORS policy
        CORS(self.app)

        # Register database brute CLI commands
        MLoader.configure_cli(self.app, db)

        self.app.logger.info('Application initialization finished!')
