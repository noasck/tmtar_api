from typing import List

from geoalchemy2 import func

from .interface import IZone
from .schema import ZoneSchema


def test_create_schema():
    assert ZoneSchema


def test_schema_works():
    result: List[IZone] = ZoneSchema(many=True).load(
        [{
            "id": "1",
            "title": "t1",
            "location_id": "1",
            "latitude": "1.123123",
            "longitude": "1.234234",
            "radius": "234"
        },
        {
            "id": "2",
            "title": "t1",
            "location_id": "1",
            "latitude": "1.123123",
            "longitude": "1.234234",
            "radius": "234"
        }],
    )

    assert result[0]['id'] == 1
    assert result[0]['title'] == 't1'
    assert result[0]['location_id'] == 1
    assert result[0]['center'] is not None
    assert result[0]['radius'] == 234
