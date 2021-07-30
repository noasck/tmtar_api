from marshmallow import Schema, fields, validate

from .constants import NAME_MAX_LENGTH, NAME_MIN_LENGTH


class LocationSchema(Schema):
    id = fields.Number(attribute='id', dump_only=True)
    name = fields.String(
        attribute='name',
        required=True,
        validate=[
            validate.NoneOf(['root']),
            validate.Length(NAME_MIN_LENGTH, NAME_MAX_LENGTH),
        ],
    )
    root = fields.Number(attribute='root', required=True)


class LocationUpdateSchema(Schema):
    name = fields.String(
        attribute='name',
        validate=[
            validate.NoneOf(['root']),
            validate.Length(NAME_MIN_LENGTH, NAME_MAX_LENGTH),
        ],
    )
