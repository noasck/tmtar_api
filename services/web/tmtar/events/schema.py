from marshmallow import Schema, fields, validate

from ..project.types import EventType
from .constants import Constants


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
        validate=validate.Length(Constants.title_min_length, Constants.title_max_length),
    )
    short_description = fields.String(
        attribute='short_description',
        required=False,
        validate=validate.Length(max=Constants.short_desc_max_length),
    )
    description = fields.String(attribute='description')
    image_file_name = fields.String(attribute='image_file_name')
    active = fields.Boolean(attribute='active')


class UpdateEventSchema(EventSchema):
    title = fields.String(
        attribute='title',
        validate=validate.Length(Constants.title_min_length, Constants.title_max_length),
    )
    event_type = fields.String(
        attribute='event_type',
        validate=validate.OneOf(EventType),
    )
