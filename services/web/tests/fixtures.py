import pytest

from services.web.project import app, db

@pytest.fixture
def app():
    return app

@pytest.fixture
def db(app):
    with app.app_context():
        db.drop_all()
        db.create_all()
        db.session.commit()
        yield db
