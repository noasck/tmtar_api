BASE_ROUTE = "locations"


def register_routes(api, app, root="api"):
    from .controller import api as location_api

    api.add_namespace(location_api, path=f"/{BASE_ROUTE}")
    print(id(api))