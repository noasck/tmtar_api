from ..injectors.accessor import TokenFixture

BASE_ROUTE = "users"



def register_routes(api, app, root="api"):
    from .controller import api as location_api

    api.add_namespace(location_api, path=f"/{root}/{BASE_ROUTE}")
    # print(id(api))
    print("imported")
    from .controller_test import create_token
    TokenFixture.inject_dependency(create_token)
