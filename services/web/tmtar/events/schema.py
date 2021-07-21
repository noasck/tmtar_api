from marshmallow import Schema, fields, validate

from ..project.types import EventType


class EventSchema(Schema):
    id = fields.Integer(attribute='id', dump_only=True)
    event_type = fields.String(
        attribute='event_type',
        validate=validate.OneOf(EventType),
        required=True,
    )
    location_id = fields.Integer(attribute='location_id')
    update_date = fields.DateTime(
        attribute='update_date',
        dump_only=True,
    )
    title = fields.String(
        attribute='title',
        required=True,
    )
    short_description = fields.String(
        attribute='short_description',
        required=True,
    )
    description = fields.String(attribute='description')
    image_file_name = fields.String(attribute='image_file_name')
    active = fields.Boolean(attribute='active')


class UpdateEventSchema(EventSchema):
    title = fields.String(
        attribute='title',
    )
    short_description = fields.String(
        attribute='short_description',
    )
    event_type = fields.String(
        attribute='event_type',
        validate=validate.OneOf(EventType),
    )
