BASE_ROUTE = "objects"


def register_routes(api, app, root="api"): # noqa
    from .controller import api as object_api

    api.add_namespace(object_api, path=f"/{root}/{BASE_ROUTE}")
