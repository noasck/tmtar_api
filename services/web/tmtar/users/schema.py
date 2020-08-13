from marshmallow import fields, Schema, validate
from ..project.types import RoleType, SexType


class UserSchema(Schema):
    id = fields.Number(attribute='id')
    email_hash = fields.String(attribute='email_hash')
    bdate = fields.Date(attribute='bdate')
    location_id = fields.Number(attribute="location_id")
    sex = fields.String(validate=validate.OneOf(SexType))
    admin_location_id = fields.Number(attribute='admin_location_id')
    role = fields.String(validate=validate.OneOf(RoleType))


class UserInfoSchema(Schema):
    bdate = fields.Date(attribute='bdate')
    location_id = fields.Number(attribute="location_id")
    sex = fields.String(validate=validate.OneOf(SexType))
