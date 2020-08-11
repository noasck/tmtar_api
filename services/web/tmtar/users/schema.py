from marshmallow import fields, Schema, validate
from marshmallow_enum import EnumField
from ..project.types import RoleType, SexType


class UserSchema(Schema):
    id = fields.Number(attribute='id')
    email_hash = fields.String(attribute='email_hash')
    age = fields.Number(attribute='age')
    location_id = fields.Number(attribute="location_id")
    sex = fields.String(validate=validate.OneOf(SexType))
    admin_location_id = fields.Number(attribute='admin_location_id')
    role = fields.String(validate=validate.OneOf(RoleType))


class UserInfoSchema(Schema):
    age = fields.Number(attribute='age')
    location_id = fields.Number(attribute="location_id")
    sex = fields.String(validate=validate.OneOf(SexType))
