from marshmallow import Schema, fields, validate

from ..project.types import SexType


class UserSchema(Schema):
    id = fields.Number(attribute='id')
    email = fields.String(attribute='email')
    bdate = fields.Date(attribute='bdate')
    location_id = fields.Number(attribute='location_id')
    sex = fields.String(
        validate=validate.OneOf(SexType),
        default=SexType[2],
        required=False,
    )
    admin_location_id = fields.Number(attribute='admin_location_id')


class UserInfoSchema(Schema):
    bdate = fields.Date(attribute='bdate')
    location_id = fields.Number(attribute='location_id')
    sex = fields.String(validate=validate.OneOf(SexType))


class UserAdminLocationIdSchema(Schema):
    admin_location_id = fields.Number(attribute='admin_location_id',
                                      required=True)
