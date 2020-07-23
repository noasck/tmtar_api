from pytest import fixture
from .model import User

@fixture
def user() -> User:
    return User(email_hash=hash("some_str"), sex="male", )