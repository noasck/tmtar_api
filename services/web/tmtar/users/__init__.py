BASE_ROUTE = "users"


def register_routes(api, app, root="api"): # noqa
    from .controller import api as location_api

    api.add_namespace(location_api, path=f"/{root}/{BASE_ROUTE}")
