from flask_restx import Api

BASE_ROUTE = 'zones'


def register_routes(api: Api, root: str = 'api'):
    """
    Register all Zone Resources.

    :param api: RestX Api instance
    :type api: Api
    :param root: base route part
    :type root: str
    """
    from .controller import api as zones_api

    api.add_namespace(zones_api, path=f'/{root}/{BASE_ROUTE}')
