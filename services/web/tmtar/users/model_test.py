from ..tests.conftest import * # noqa
from pytest import fixture
from .model import User
from ..project.types import *
from datetime import datetime


@fixture
def user() -> User:
    return User(email=str(hash("some_str")), sex=SexType[0], bdate=datetime.now().date(),
                location_id=1)


def test_create_model(user: User):
    assert user
