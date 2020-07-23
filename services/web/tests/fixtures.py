import pytest


@pytest.fixture
def app():
    from ..project import app
    return app

@pytest.fixture
def db(app):
    from ..project import db
    with app.app_context():
        db.drop_all()
        db.create_all()
        yield db
        db.session.commit()
