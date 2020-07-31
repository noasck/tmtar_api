from marshmallow import fields, Schema
from marshmallow_enum import EnumField
from ..project.types import RoleType, SexType


class UserSchema(Schema):
    id = fields.Number(attribute='id')
    email_hash = fields.String(attribute='email_hash')
    age = fields.Number(attribute='age')
    location_id = fields.Number(attribute="location_id")
    sex = EnumField(SexType, by_value=True)
    role = EnumField(RoleType, by_value=True)
    admin_location_id = fields.Number(attribute='admin_location_id')


class UserInfoSchema(Schema):
    age = fields.Number(attribute='age')
    location_id = fields.Number(attribute="location_id")
    sex = EnumField(SexType, by_value=True)
