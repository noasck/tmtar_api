from geoalchemy2 import func, shape
from marshmallow import Schema, fields, post_load, pre_dump, validate

from .model import Zone

latitude_field = 'latitude'
longitude_field = 'longitude'
latitude_limit = 90
longitude_limit = 180
max_radius = 2000


class ZoneSchema(Schema):
    """Zone instance schema."""

    id = fields.Integer(attribute='id')
    title = fields.String(attribute='title', required=True)
    location_id = fields.Integer(attribute='location_id', required=True)
    latitude = fields.Float(
        attribute=latitude_field,
        validate=validate.Range(-latitude_limit, latitude_limit),
        required=True,
    )
    longitude = fields.Float(
        attribute=longitude_field,
        validate=validate.Range(-longitude_limit, longitude_limit),
        required=True,
    )
    radius = fields.Float(
        attribute='radius',
        required=True,
        validate=validate.Range(0, max_radius),
    )
    active = fields.Boolean(attribute='active')
    secret = fields.Boolean(attribute='secret')

    @post_load
    def make_point(self, load_data: dict, **kwargs):
        """Make a point from latitude and longitude."""
        load_data['center'] = func.ST_MakePoint(
            load_data[longitude_field],
            load_data[latitude_field],
        )
        load_data.pop(latitude_field)
        load_data.pop(longitude_field)
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
        attribute=latitude_field,
        validate=validate.Range(-latitude_limit, latitude_limit),
    )
    longitude = fields.Float(
        attribute=longitude_field,
        validate=validate.Range(-longitude_limit, longitude_limit),
    )
    radius = fields.Float(
        attribute='radius',
        validate=validate.Range(0, max_radius),
    )

    @post_load
    def make_point(self, load_data: dict, **kwargs):
        """Make a point from latitude and longitude."""
        if longitude_field in load_data.keys() and latitude_field in load_data.keys():
            load_data['center'] = func.ST_MakePoint(
                load_data[longitude_field],
                load_data[latitude_field],
            )

        if longitude_field in load_data.keys():
            load_data.pop(longitude_field)

        if latitude_field in load_data.keys():
            load_data.pop(latitude_field)

        return load_data
