from pytest import fixture
from .model import User
from ..project.types import *

@fixture
def user() -> User:
    return User(email_hash=hash("some_str"), sex=SexType.MALE, age=14, location_id=1, role=RoleType.COMMON)


def test_create_model(user: User):
    assert user
