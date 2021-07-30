from typing import List

from flask_sqlalchemy import SQLAlchemy
from geoalchemy2 import func
from geoalchemy2.elements import WKTElement

from ..tests.fixtures import *
from .interface import IZone
from .model import Zone
from .schema import ZoneSchema, ZoneUpdateSchema


def test_create_schema():
    assert ZoneSchema


def test_update_schema():
    return ZoneUpdateSchema


def test_schema_works():
    result: List[IZone] = ZoneSchema(many=True).load(
        [{
            "title": "sample_title1",
            "location_id": "1",
            "latitude": "1.123123",
            "longitude": "1.234234",
            "radius": "234"
        },

        {
            "title": "sample_title1",
            "location_id": "1",
            "latitude": "1.123123",
            "longitude": "1.234234",
            "radius": "234"
        }],
    )

    assert result[0]['title'] == 'sample_title1'
    assert result[0]['location_id'] == 1
    assert result[0]['center'] is not None
    assert result[0]['radius'] == 234


def test_schema_dumps():
    result = ZoneSchema().dump(
        Zone(
            id=1,
            title="Abstract title",
            location_id=1,
            active=True,
            radius=123,
            center=WKTElement('POINT(3.546456 45.6567456)', srid=4326),
        )
    )
    assert result['latitude'] == 45.6567456
    assert result['longitude'] == 3.546456


def test_schema_dumps_from_db(db: SQLAlchemy):
    z1 = Zone(
        id=1,
        title="Abstract title",
        location_id=1,
        active=True,
        radius=123,
        center=func.ST_MakePoint(3.546456, 45.6567456),
    )

    db.session.add(z1)
    db.session.commit()

    z1 = Zone.query.get(1)
    result = ZoneSchema().dump(z1)
    assert result['latitude'] == 45.6567456
    assert result['longitude'] == 3.546456


def test_update_schema_works():
    result: List[IZone] = ZoneUpdateSchema(many=True).load(
        [
            {
                "title": "sample_title1",
                "longitude": "34.234234",
                "latitude": "34.3242342",
            },
            {
                "title": "sample_title1",
                "longitude": "34.234234",
            },
            {
                "title": "sample_title1",
                "latitude": "34.3242342",
            }
        ]
    )

    assert result[0]['center'] is not None
    assert 'longitude' not in result[1].keys()
    assert 'latitude' not in result[2].keys()
