from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from flask import Flask


class ModulesSetupLoader:
    """Setups all app modules."""

    @staticmethod
    def configure_jwt(app: Flask) -> JWTManager:
        """Configuring JSON web token plugin."""
        return JWTManager(app)

    @staticmethod
    def configure_db(app: Flask) -> SQLAlchemy:
        """Configuring SQLAlchemy ORM plugin."""
        db = SQLAlchemy(app)
        return db

    @staticmethod
    def configure_ma(app: Flask) -> Marshmallow:
        """Configuring Marshmallow plugin."""
        ma = Marshmallow(app)
        return ma

    @staticmethod
    def configure_api(app: Flask) -> Api:
        """Configuring Flask RestX plugin."""
        doc = "/"
        if app.config['FLASK_ENV'] == 'production':
            doc = False
        api = Api(app, app.config["API_TITLE"], doc=doc)
        return api

    @staticmethod
    def tables_db_init(app: Flask, db: SQLAlchemy) -> None:
        """
        Recreates database.
        @param app: main Flask app.
        @param db: db connection instance.
        """
        from .seed_db import seed_db

        if app.config["INIT_DB"]:
            app.logger.info('Initializing database tables...')
            # TODO: dump database records for debug or preprocessing.
            db.session.remove()
            db.drop_all()
            db.session.commit()
            db.create_all()
            db.session.commit()
            db.session.commit()

            for email in seed_db():
                app.logger.info(f"Successfully seeded {email} root user.")

            app.logger.info('Initializing database tables - OK.')
        else:
            app.logger.info('Skipping init db tables...')

    @staticmethod
    def configure_health_route(app: Flask):
        """
        Adds /health route to check server status.
        @param app: main Flask app.
        """
        @app.route('/health', methods=['GET'])
        def health():
            return "Healthy"
