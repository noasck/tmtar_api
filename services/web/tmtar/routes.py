from .locations import register_routes as add_location_routing


def register_routes(api, app):
    add_location_routing(api, app)
