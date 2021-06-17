from flask_restx import Api

from .events import register_routes as add_event_routing
from .files import register_routes as add_file_routing
from .locations import register_routes as add_location_routing
from .objects import register_routes as add_object_routing
from .users import register_routes as add_user_routing


def register_routes(api: Api):
    """
    Register all application RESTX Resources.

    :param api:  RestX Api instance
    :type api: Api
    """
    add_location_routing(api)
    add_user_routing(api)
    add_file_routing(api)
    add_object_routing(api)
    add_event_routing(api)
