from unittest.mock import patch

import pytest
from flask.testing import FlaskClient
from flask_sqlalchemy import SQLAlchemy
from geoalchemy2 import func
from geoalchemy2.types import WKTElement

from ..files.model import File
from ..project.types import EventType
from ..tests.fixtures import *  # noqa
from . import BASE_ROUTE
from .interface import IZone
from .model import Zone
from .schema import ZoneSchema, ZoneUpdateSchema
from .service import SecureZoneService


def create_zone(
    zone_id=1,
    title="Sample_title",
    location_id=1,
    center=WKTElement('POINT(3.546456 45.6567456)', srid=4326),
    radius: float = 10.0,
    active=True,
    secret=False
) -> IZone:
    return IZone(
        id=zone_id,
        title=title,
        location_id=location_id,
        center=center,
        radius=radius,
        active=active,
        secret=secret,
    )


def make_update(zone_id, zone_upd: IZone, *args, **kwargs) -> Zone:
    new_zone = Zone(**create_zone(zone_id, title=zone_upd['title'], radius=zone_upd['radius']))
    return new_zone


def represent_created_zone(zone: Zone):
    zone.center = WKTElement('POINT(3.546456 45.6567456)', srid=4326)
    return zone


class TestZonesResource:

    @patch.object(SecureZoneService, "get_by_location_id", lambda *args, **kwargs: [
        Zone(**create_zone(1, title='zone1')),
        Zone(**create_zone(2, title='zone2'))
    ])
    def test_get(self, client: FlaskClient, token):
        with client:
            result = client.get(
                f"/api/{BASE_ROUTE}",
                headers={
                    "Authorization": f"Bearer {token}"
                },
                follow_redirects=True,
            ).get_json()
            expected = (ZoneSchema(many=True).dump([
                Zone(**create_zone(1, title='zone1')),
                Zone(**create_zone(2, title='zone2'))
            ]))
            assert result == expected

    @patch.object(SecureZoneService, "create",
                  lambda create_request, *args, **kwargs: represent_created_zone(Zone(**create_request)))
    def test_post(self, client: FlaskClient, token: str):
        with client:
            result = client.post(
                f"/api/{BASE_ROUTE}/",
                json={
                    'id': 1,
                    'title': 'zone1',
                    'longitude': '3.546456',
                    'latitude': '45.6567456',
                    'location_id': '1',
                    'radius': '10',
                    'secret': False,
                    'active': True
                },
                headers={
                    "Authorization": f"Bearer {token}"
                }
            ).get_json()
            expected = (ZoneSchema().dump(
                Zone(**create_zone(zone_id=1, title='zone1'))
            ))
            assert result == expected

class TestZoneIDResource:
    @patch.object(SecureZoneService, "delete_by_id",
                  lambda zone_id, *args, **kwargs: zone_id)
    def test_delete(self, client: FlaskClient, token: str):
        with client:
            result = client.delete(f"/api/{BASE_ROUTE}/2",
                                   headers={
                                       "Authorization": f"Bearer {token}"
                                   }).get_json()
            expected = dict(status="Success", id=2)
            assert result == expected

    @patch.object(SecureZoneService, 'update_by_id', make_update)
    def test_put(self, client: FlaskClient, token: str):
        with client:
            result = client.put(
                f'/api/{BASE_ROUTE}/1',
                json={
                    'title': 'sample_new_title',
                    'radius': '234'
                },
                headers={
                    "Authorization": f"Bearer {token}"
                }
            ).get_json()

            expected = (ZoneSchema().dump(
                Zone(**create_zone(zone_id=1, title='sample_new_title', radius=234))))

            assert result == expected
