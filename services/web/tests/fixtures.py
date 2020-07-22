import pytest

from ..project import app as imported_app

@pytest.fixture
def app():
    return imported_app

@pytest.fixture
def db(app):
    from ..project import db
    with app.app_context():
        db.create_all()
        yield db
        db.drop_all()
        db.session.commit()
