from marshmallow import Schema, fields


class ObjectSchema(Schema):
    id = fields.Number(attribute="id")
    name = fields.String(attribute="name")
    target_image_file = fields.String(attribute="target_image_file")
    asset_file = fields.String(attribute="asset_file")
    subzone_id = fields.Number(attribute="subzone_id")
