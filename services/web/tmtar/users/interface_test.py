from ..tests.fixtures import *
from pytest import fixture
from .model import User
from .interface import IUser


@fixture
def interface() -> IUser:
    return IUser(email_hash=hash("some_str"), sex="male", age=14, location_id=1, role="common")


def test_interface_create(interface: IUser):
    assert interface


def test_interface_works(interface: IUser):
    user = User(**interface)
    assert user
