from ..injectors.accessor import LocationChecker

BASE_ROUTE = "locations"


def register_routes(api, app, root="api"): # noqa
    from .controller import api as location_api

    api.add_namespace(location_api, path=f"/{root}/{BASE_ROUTE}")
    from .service import LocationService
    LocationChecker.inject_dependency(LocationService.check_location_permission)
