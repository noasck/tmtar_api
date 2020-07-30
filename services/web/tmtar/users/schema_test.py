from ..tests.fixtures import *
from pytest import fixture

from .model import User
from .schema import UserSchema
from .interface import IUser, RoleType, SexType


@fixture
def schema() -> UserSchema:
    return UserSchema()


def test_LocationSchema_create(schema: UserSchema):
    assert schema


def test_LocationSchema_works(schema: UserSchema):
    params: IUser = schema.load(
        {
            'email_hash': str(hash("some_str")),
            'sex': "male",
            'age': '14',
            'location_id': '1',
            'role': "common user"

        }
    )
    widget = User(**params)

    assert widget.email_hash == str(hash("some_str"))
    assert widget.sex == SexType.MALE.value
    assert widget.age == 14
    assert widget.location_id == 1
    assert widget.role == RoleType.COMMON.value
