from marshmallow import fields, Schema


class FileSchema(Schema):
    id = fields.Number(attribute='id')
    filename = fields.String(attribute='filename')
