BASE_ROUTE = "files"


def register_routes(api, app, root="api"): # noqa
    from .controller import api as files_api

    api.add_namespace(files_api, path=f"/{root}/{BASE_ROUTE}")
