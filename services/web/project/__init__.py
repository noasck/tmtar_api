from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import werkzeug
werkzeug.cached_property = werkzeug.utils.cached_property
from flask_restplus import Api, Resource
from flask_restplus import Api, Resource

app = Flask(__name__)

app.config.from_object("app.project.config.Config")

api = Api(app)
ma = Marshmallow(app)
db = SQLAlchemy(app)

@api.route('/hello/')
class HelloWorld(Resource):
    def get(self):
        return "Hello World"
