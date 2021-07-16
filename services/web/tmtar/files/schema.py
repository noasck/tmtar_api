from marshmallow import Schema, fields


class FileSchema(Schema):
    id = fields.Number(attribute='id', dump_only=True)
    filename = fields.String(attribute='filename')
