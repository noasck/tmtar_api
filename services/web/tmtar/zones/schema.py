from geoalchemy2 import func, shape
from marshmallow import Schema, fields, post_load, pre_dump, validate

from .constants import Constants
from .model import Zone


class ZoneSchema(Schema):
    """Zone instance schema."""

    id = fields.Integer(attribute='id', dump_only=True)
    title = fields.String(
        attribute='title',
        required=True,
        validate=validate.Length(Constants.title_min_length, Constants.title_max_length),
    )
    location_id = fields.Integer(attribute='location_id', required=True)
    latitude = fields.Float(
        attribute=Constants.latitude_field,
        validate=validate.Range(-Constants.latitude_limit, Constants.latitude_limit),
        required=True,
    )
    longitude = fields.Float(
        attribute=Constants.longitude_field,
        validate=validate.Range(-Constants.longitude_limit, Constants.longitude_limit),
        required=True,
    )
    radius = fields.Float(
        attribute='radius',
        required=True,
        validate=validate.Range(Constants.min_radius, Constants.max_radius),
    )
    active = fields.Boolean(attribute='active')
    secret = fields.Boolean(attribute='secret')
    description = fields.String(
        attribute='description',
        validate=validate.Length(max=Constants.description_max_length),
    )
    actual_address = fields.String(attribute='actual_address')
    preview_image_filename = fields.String(attribute='preview_image_filename')

    @post_load
    def make_point(self, load_data: dict, **kwargs):
        """Make a point from latitude and longitude."""
        load_data['center'] = func.ST_MakePoint(
            load_data[Constants.longitude_field],
            load_data[Constants.latitude_field],
        )
        load_data.pop(Constants.latitude_field)
        load_data.pop(Constants.longitude_field)
        return load_data

    @pre_dump
    def long_lat_form_point(self, dump_data: Zone, **kwargs):
        """Extract latitude and longitude from geometry center."""
        point = shape.to_shape(dump_data.center)
        dump_data.latitude = point.y
        dump_data.longitude = point.x
        return dump_data


class ZoneUpdateSchema(ZoneSchema):
    """Zone schema with no required fields."""

    title = fields.String(attribute='title')
    location_id = fields.Integer(attribute='location_id')
    latitude = fields.Float(
        attribute=Constants.latitude_field,
        validate=validate.Range(-Constants.latitude_limit, Constants.latitude_limit),
    )
    longitude = fields.Float(
        attribute=Constants.longitude_field,
        validate=validate.Range(-Constants.longitude_limit, Constants.longitude_limit),
    )
    radius = fields.Float(
        attribute='radius',
        validate=validate.Range(Constants.min_radius, Constants.max_radius),
    )

    @post_load
    def make_point(self, load_data: dict, **kwargs):
        """Make a point from latitude and longitude."""
        latitude_presence = Constants.latitude_field in load_data.keys()
        longitude_presence = Constants.longitude_field in load_data.keys()

        if latitude_presence and longitude_presence:
            load_data['center'] = func.ST_MakePoint(
                load_data[Constants.longitude_field],
                load_data[Constants.latitude_field],
            )

        if longitude_presence:
            load_data.pop(Constants.longitude_field)

        if latitude_presence:
            load_data.pop(Constants.latitude_field)

        return load_data
