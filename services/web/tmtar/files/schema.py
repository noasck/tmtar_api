from marshmallow import fields, Schema, validate


class FileSchema(Schema):
    id = fields.Number(attribute='id')
    filename = fields.String(attribute='filename')

