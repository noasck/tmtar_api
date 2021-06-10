import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))

# TODO: rewrite and remove config to yml. Add validation,


class Config(object):
    API_TITLE = 'Take Me To AR API'
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    FLASK_ENV = os.getenv('FLASK_ENV')
    MEDIA_FOLDER = f"{os.getenv('APP_FOLDER')}/project/media"  # noqa: WPS237,E501
    PROPAGATE_EXCEPTIONS = True

    if FLASK_ENV == 'production':  # noqa: WPS604
        AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')
        ALGORITHMS = os.getenv('ALGORITHMS')
        API_AUDIENCE = os.getenv('API_AUDIENCE')
        JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
        JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)
    else:
        JWT_ACCESS_TOKEN_EXPIRES = False
        JWT_REFRESH_TOKEN_EXPIRES = False
