from .locations import register_routes as add_location_routing
from .users import register_routes as add_user_routing
from .files import register_routes as add_file_routing


def register_routes(api, app):
    add_location_routing(api, app)
    add_user_routing(api, app)
    add_file_routing(api, app)
