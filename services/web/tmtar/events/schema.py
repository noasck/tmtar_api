from marshmallow import Schema, fields, validate

from ..project.types import EventType, SexType


class EventSchema(Schema):
    id = fields.Integer(attribute='id')
    event_type = fields.String(
        attribute='event_type',
        validate=validate.OneOf(EventType),
    )
    location_id = fields.Integer(attribute='location_id')
    update_date = fields.Integer(
        attribute='update_date',
        validate=validate.Range(min=1597401274),
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
