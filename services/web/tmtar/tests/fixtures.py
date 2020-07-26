import pytest
from ..project import create_app
create_app(True)

@pytest.fixture
def app():
    from ..project import FlaskApp
    return FlaskApp


@pytest.fixture
def db(app):
    return app.Instance().init_db()

@pytest.fixture
def client(app):
    return app.Instance().client_app()
