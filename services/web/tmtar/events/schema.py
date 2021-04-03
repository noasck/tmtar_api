from marshmallow import Schema, fields, validate

from ..project.types import EventType, SexType


class EventSchema(Schema):
    id = fields.Integer(attribute='id')
    event_type = fields.String(attribute='event_type',
                               validate=validate.OneOf(EventType))
    location_id = fields.Integer(attribute='location_id')
    update_date = fields.Integer(attribute='update_date',
                                 validate=validate.Range(min=1597401274))
    sex = fields.String(attribute='sex', validate=validate.OneOf(SexType))
    min_age = fields.Integer(attribute='min_age',
                             validate=validate.Range(min=0, max=100))
    max_age = fields.Integer(attribute='max_age',
                             validate=validate.Range(min=0, max=150))
    title = fields.String(attribute='title')
    short_description = fields.String(attribute='short_description')
    description = fields.String(attribute='description')
    image_file_name = fields.String(attribute='image_file_name')
    active = fields.Boolean(attribute='active')
