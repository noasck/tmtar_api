import pytest
from ..injectors.accessor import Fixtures


@pytest.fixture
def app():
    from ..injectors.app import FlaskApp
    return FlaskApp


@pytest.fixture
def db(app):
    return app.Instance().init_db()


@pytest.fixture
def client(app):
    return app.Instance().client_app()


@pytest.fixture
def token(client):
    return Fixtures.get("create_token")(client)
