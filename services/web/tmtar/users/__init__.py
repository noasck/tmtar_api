from ..injectors.accessor import Fixtures

BASE_ROUTE = "users"


def register_routes(api, app, root="api"): # noqa
    from .controller import api as location_api

    api.add_namespace(location_api, path=f"/{root}/{BASE_ROUTE}")
    from .controller_test import create_token
    Fixtures.inject_dependency(create_token)
    print("TokenFixture imported successfully")
