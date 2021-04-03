from flask import Flask
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy


class ModulesSetupLoader(object):
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
    }

    @classmethod
    def configure_jwt(cls, app: Flask) -> JWTManager:
        """Configure JSON web token plugin."""
        return JWTManager(app)

    @classmethod
    def configure_db(cls, app: Flask) -> SQLAlchemy:
        """Configure SQLAlchemy ORM plugin."""
        return SQLAlchemy(app)

    @classmethod
    def configure_ma(cls, app: Flask) -> Marshmallow:
        """Configure Marshmallow plugin."""
        return Marshmallow(app)

    @classmethod
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
    def tables_db_init(cls, app: Flask, db: SQLAlchemy) -> None:
        """
        Recreate database.
        :param app: main Flask app.
        :type app: Flask
        :param db: db connection instance.
        :type db: SQLAlchemy
        """
        from .seed_db import seed_db
        if app.config['INIT_DB']:
            app.logger.info('Initializing database tables...')
            # TODO: dump database records for debug or preprocessing.
            db.session.remove()
            db.drop_all()
            db.session.commit()
            db.create_all()
            db.session.commit()

            for email in seed_db():
                app.logger.info(f'Successfully seeded {email} root user.')

            app.logger.info('Initializing database tables - OK.')
        else:
            app.logger.info('Skipping init db tables...')

    @classmethod
    def configure_health_route(cls, app: Flask):
        """
        Add /health route to check server status.
        :param app: main Flask app.
        """
        @app.route('/health', methods=['GET'])
        def health():
            return 'Healthy'
