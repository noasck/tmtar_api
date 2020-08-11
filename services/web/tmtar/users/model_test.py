from pytest import fixture
from .model import User
from ..project.types import *

@fixture
def user() -> User:
    return User(email_hash=str(hash("some_str")), sex=SexType[0], age=14, location_id=1, role=RoleType[0])


def test_create_model(user: User):
    assert user
