from pytest import fixture

from .project import create_app
from .injectors.app import FlaskApp

app = create_app(True).Instance()


@fixture
def flaskApp() -> FlaskApp.WrappedFlaskApp: # noqa
    return app


def test_create_app(flaskApp: FlaskApp.WrappedFlaskApp): # noqa
    assert flaskApp