from . import *
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_restplus import Api
from flask_sqlalchemy import SQLAlchemy


class FlaskApp:
    '''Wrapper for Flask App Instance'''

    class WrappedFlaskApp:
        def __init__(self, config: str, api_title: str, test: bool = False):
            self.__app = Flask(__name__)
            self.__app.config.from_object(config)
            self.__jwt = JWTManager(self.__app)
            self.__db = SQLAlchemy(self.__app)

            if test:
                self.init_db()

            self.__api = Api(self.__app, api_title)
            self.__ma = Marshmallow(self.__app)

        @property
        def jwt(self):
            return self.__jwt

        def register_routes(self, register_routes):
            '''
            Executing function implements internal routing
            :param register_routes: lambda from route.py
            :return: None
            '''
            register_routes(self.__api, self.__app)

        def init_db(self):
            self.__db.session.remove()
            self.__db.drop_all()
            self.__db.create_all()
            self.__db.session.commit()
            return self.__db

        def client_app(self):
            return self.__app.test_client()

        @property
        def database(self):
            return self.__db

        def run(self, **kwargs):
            self.__app.run(**kwargs)

    __instance = None

    def __init__(self):
        ''' Singleton: not implemented'''
        raise NotImplementedError('Singleton doesn\'t inmplements constructor initialization')

    @staticmethod
    def Instance(*args) -> WrappedFlaskApp:
        ''' :return instance of WrappedFlaskApp class with app and db '''

        print("calling #")

        if not FlaskApp.__instance:
            FlaskApp.__instance = FlaskApp.WrappedFlaskApp(*args)
            print(id(FlaskApp.__instance))

        return FlaskApp.__instance