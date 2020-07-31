from ..tests.fixtures import *
from pytest import fixture

from .model import User
from .schema import UserSchema, UserInfoSchema
from .interface import IUser, RoleType, SexType


@fixture
def schema() -> UserSchema:
    return UserSchema()


@fixture
def info_schema() -> UserInfoSchema:
    return UserInfoSchema()


def test_UserSchema_create(schema: UserSchema):
    assert schema


def test_UserSchema_works(schema: UserSchema):
    params: IUser = schema.load(
        {
            'email_hash': str(hash("some_str")),
            'sex': SexType.MALE,
            'age': '14',
            'location_id': '1',
            'role': RoleType.COMMON

        }
    )
    widget = User(**params)

    assert widget.email_hash == str(hash("some_str"))
    assert widget.sex == SexType.MALE
    assert widget.age == 14
    assert widget.location_id == 1
    assert widget.role == RoleType.COMMON


def test_UserInfoSchema_create(info_schema: UserInfoSchema):
    assert info_schema
