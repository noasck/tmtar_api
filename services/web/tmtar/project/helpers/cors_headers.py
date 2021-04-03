from flask import Flask
from flask_cors import CORS


def register_cors(app: Flask):
    """
    Implement CORS headers policy middleware.
    :param app: main Flask object
    """
    CORS(app)
