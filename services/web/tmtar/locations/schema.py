from marshmallow import fields, Schema, validate


class LocationSchema(Schema):
    id = fields.Number(attribute='id')
    name = fields.String(attribute='name', required=True, validate=validate.NoneOf(['root']))
    root = fields.Number(attribute='root', required=False)


class LocationUpdateSchema(Schema):
    id = fields.Number(attribute='id')
    name = fields.String(attribute='name', required=True, validate=validate.NoneOf(['root']))
