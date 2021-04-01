import werkzeug
werkzeug.cached_property = werkzeug.utils.cached_property # noqa

from flask import Flask
from tmtar import * # noqa
from tmtar.project import AppModule # noqa


def start_app() -> Flask:
    """App class Factory method."""
    app = AppModule().configure()
    return app


if __name__ == "__main__":
    flask_app: Flask = start_app()
    flask_app.run(host='0.0.0.0', debug=False)
