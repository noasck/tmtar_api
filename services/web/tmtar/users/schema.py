from marshmallow import fields, Schema


class UserSchema(Schema):
    id = fields.Number(attribute='id')
    email_hash = fields.String(attribute='email_hash')
    age = fields.Number(attribute='age')
    location_id = fields.Number(attribute="location_id")
    sex = fields.String(attribute='sex')
    role = fields.String(attribute='role')
    admin_location_id = fields.Number(attribute='admin_location_id')
