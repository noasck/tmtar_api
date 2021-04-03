from flask_restx import Api

from ..project.injector import Injector

BASE_ROUTE = 'locations'


def register_routes(api: Api, root: str = 'api'):
    """
    Register all Location Resources.

    :param api: RestX Api instance
    :type api: Api
    :param root: base route part
    :type root: str
    """
    from .controller import api as location_api

    api.add_namespace(location_api, path=f'/{root}/{BASE_ROUTE}')

    from .service import LocationService
    Injector.inject(LocationService, to='LocationService')
