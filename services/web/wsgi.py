"""Main app entry point."""
import flask
import werkzeug

# monkey patching
werkzeug.cached_property = werkzeug.utils.cached_property  # noqa: E402
flask.helpers._endpoint_from_view_func = flask.scaffold._endpoint_from_view_func  # noqa: E402, WPS437, E501

from tmtar.project import AppModule  # noqa: F401, E402


def start_app() -> flask.Flask:
    """
    App class Factory method.

    :return: main flask app object
    """
    return AppModule().app


if __name__ == '__main__':
    flask_app: flask.Flask = start_app()
    flask_app.run(host='0.0.0.0', debug=False)
