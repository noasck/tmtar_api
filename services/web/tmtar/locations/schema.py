from marshmallow import fields, Schema


class LocationSchema(Schema):
    id = fields.Number(attribute='id')
    name = fields.String(attribute='name')
    root = fields.Number(attribute='root')
