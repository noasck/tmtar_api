from flask import Flask
from flask_restx import Api

from .locations import register_routes as add_location_routing
from .users import register_routes as add_user_routing
from .files import register_routes as add_file_routing
from .objects import register_routes as add_object_routing


def register_routes(api: Api, app: Flask):
    """
    Registering all modules and instances.
    @param api: RestX Api instance.
    @param app: main Flask app.
    """
    add_location_routing(api, app)
    add_user_routing(api, app)
    add_file_routing(api, app)
    add_file_routing(api, app)
    add_object_routing(api, app)
