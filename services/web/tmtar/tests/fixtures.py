import pytest
from wsgi import start_app  # noqa

from ..project.helpers.ext_loader import ModulesSetupLoader
from ..project.injector import Injector

try:
    Injector.db
except AttributeError:
    start_app()


@pytest.fixture
def app():
    return Injector.app


@pytest.fixture
def db(app):
    db = Injector.db
    ModulesSetupLoader.tables_db_init(app, db)
    return db


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def token(client):
    from ..users.controller_test import create_token

    return create_token(client)
