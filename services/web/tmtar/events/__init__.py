from flask_restx import Api

BASE_ROUTE = 'events'


def register_routes(api: Api, root: str = 'api'):
    """
    Register all Events Resources.

    :param api: RestX Api instance
    :type api: Api
    :param root: base route part
    :type root: str
    """
    from .controller import api as events_api

    api.add_namespace(events_api, path=f'/{root}/{BASE_ROUTE}')
