from ..injectors.app import FlaskApp


def create_app(test: bool=False):
    config = "tmtar.project.config.Config"
    api_title = "Take Me To AR API"
    app = FlaskApp.Instance(config, api_title, test)
    from ..routes import register_routes
    app.register_routes(register_routes)
    return FlaskApp


