from ..tests.fixtures import * # noqa
from pytest import fixture
from .model import User
from .interface import IUser


@fixture
def interface() -> IUser:
    return IUser(email_hash=str(hash("some_str")), sex="male", bdate='2016-02-03', location_id=1, role="common")


def test_interface_create(interface: IUser):
    assert interface


def test_interface_works(interface: IUser):
    user = User(**interface)
    assert user
