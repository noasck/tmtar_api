import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    API_TITLE = "Take Me To AR API"
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    FLASK_ENV = os.getenv("FLASK_ENV")
    MEDIA_FOLDER = f"{os.getenv('APP_FOLDER')}/project/media"
    INIT_DB = bool(os.getenv('DB_INIT'))
