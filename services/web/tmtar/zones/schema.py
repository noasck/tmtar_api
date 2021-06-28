from geoalchemy2 import func
from marshmallow import Schema, fields, post_load, validate


class ZoneSchema(Schema):
    """Zone instance schema."""

    id = fields.Integer(attribute='id')
    title = fields.String(attribute='title', required=True)
    location_id = fields.Integer(attribute='location_id', required=True)
    latitude = fields.Float(
        attribute='latitude',
        validate=validate.Range(-90, 90),
        required=True,
    )
    longitude = fields.Float(
        attribute='longitude',
        validate=validate.Range(-180, 180),
        required=True
    )
    radius = fields.Float(
        attribute='radius',
        required=True,
        validate=validate.Range(0, 2000),
    )
    active = fields.Boolean(attribute='active')
    secret = fields.Boolean(attribute='secret')

    @post_load
    def make_point(self, data: dict, **kwargs):
        """Make a point from latitude and longitude."""
        data['center'] = func.ST_MakePoint(data['longitude'], data['latitude'])
        del data['latitude']
        del data['longitude']
        return data
