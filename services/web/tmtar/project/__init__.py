from ..injectors.app import FlaskApp


def create_app(test: bool = False):
    config = "tmtar.project.config.Config"
    api_title = "Take Me To AR API"
    FlaskApp.Instance(config, api_title, test)
    return FlaskApp
