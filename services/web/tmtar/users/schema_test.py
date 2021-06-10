from datetime import datetime

from pytest import fixture

from ..project.types import SexType
from ..tests.fixtures import *  # noqa
from .interface import IUser
from .model import User
from .schema import UserAdminLocationIdSchema, UserInfoSchema, UserSchema


@fixture
def schema() -> UserSchema:
    return UserSchema()


@fixture
def info_schema() -> UserInfoSchema:
    return UserInfoSchema()


@fixture
def admin_loc_id_schema() -> UserAdminLocationIdSchema:
    return UserAdminLocationIdSchema()

def test_UserSchema_create(schema: UserSchema):  # noqa
    assert schema


def test_UserSchema_works(schema: UserSchema):  # noqa
    params: IUser = schema.load({
        'identity': str(hash("some_str")),
        'sex': SexType[0],
        'bdate': '2016-02-03',
        'location_id': '1',
    })
    widget = User(**params)

    assert widget.identity == str(hash("some_str"))
    assert widget.sex == SexType[0]
    assert widget.bdate == datetime.strptime("2016-02-03", "%Y-%m-%d").date()
    assert widget.location_id == 1


def test_UserInfoSchema_create(info_schema: UserInfoSchema):  # noqa
    assert info_schema


def test_UserAdminLocationIdSchema_create(admin_loc_id_schema: UserAdminLocationIdSchema):  # noqa
    assert admin_loc_id_schema
