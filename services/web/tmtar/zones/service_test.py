from datetime import datetime
from typing import List
from unittest.mock import patch

import pytest
from flask_sqlalchemy import SQLAlchemy
from geoalchemy2 import func

from ..files.model import File
from ..project.types import EventType
from ..tests.fixtures import app, db  # noqa
from .interface import IZone
from .model import Zone
from .service import LocationAccessError, LocationService, SecureZoneService

time_now = datetime.utcnow()


def create_zone(
    zone_id=1,
    title="Sample_title",
    location_id=1,
    center=func.ST_MakePoint(34.234234, 23.234234),
    radius=10,
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


@patch.object(LocationService, 'get_all_ancestors_id', lambda *args: [2, 3])
def test_get_zones_by_location(db: SQLAlchemy):
    LocationService.create({"id": 2, "name": "loc1", "root": 1})
    LocationService.create({"id": 3, "name": "loc2", "root": 2})

    z1 = Zone(**create_zone(zone_id=1, location_id=1))
    z2 = Zone(**create_zone(zone_id=2, location_id=2))
    z3 = Zone(**create_zone(zone_id=3, location_id=3))

    db.session.add_all([z1, z2, z3])
    db.session.commit()

    result = SecureZoneService.get_by_location_id(2)

    assert len(result) == 2
    assert z2 in result
    assert z3 in result


class TestSecuredZoneUpdate:
    """
        Testing update Zone functionality.

        Cases:
        + Case 1: has access to location. No location_id update.
        - Case 2: has NO access to location. Exception.
        + Case 3: has access to location and updated location.
        - Case 4: has NO access to updated location. Exception.
        """

    @patch.object(LocationService, 'has_permission', lambda *args: True)
    def test_case1(self, db: SQLAlchemy):
        event_upd = IZone(title='Wubba lubba')
        event = Zone(**create_zone(zone_id=1))

        db.session.add(event)
        db.session.commit()

        SecureZoneService.update_by_id(event.id, event_upd, 1)
        events = Zone.query.all()

        assert len(events) == 1

        assert events[0].title == 'Wubba lubba'

    @patch.object(LocationService, 'has_permission', lambda *args: False)
    def test_case2(self, db: SQLAlchemy):
        event_upd = Zone(title='dfgdfg')
        event = Zone(**create_zone(zone_id=1))

        db.session.add(event)
        db.session.commit()

        try:
            SecureZoneService.update_by_id(event.id, event_upd, 1)
        except LocationAccessError:
            assert True

    @patch.object(LocationService, 'has_permission', lambda *args: True)
    def test_case3(self, db: SQLAlchemy):
        event_upd = IZone(active=True, title='Wubba Lubba', location_id=2)
        event = Zone(**create_zone())

        LocationService.create({"id": 2, "name": "loc1", "root": 1})

        db.session.add(event)
        db.session.commit()

        SecureZoneService.update_by_id(event.id, event_upd, 1)
        events = Zone.query.all()

        assert len(events) == 1

        assert events[0].title == 'Wubba Lubba'

        assert events[0].location_id == 2

    # returns True for first check and False for second (see Service class).
    @patch.object(LocationService, 'has_permission', lambda l1, l2: l2 == 42)
    def test_case4(self, db: SQLAlchemy):
        event_upd = create_zone(active=True, title='Wubba Lubba', location_id=2)
        event = Zone(**create_zone(active=False))

        LocationService.create({"id": 2, "name": "loc1", "root": 1})

        db.session.add(event)
        db.session.commit()

        try:
            SecureZoneService.update_by_id(event.id, event_upd, 42)
        except LocationAccessError:
            assert True


@patch.object(LocationService, "has_permission", lambda *args: True)
def test_create(db: SQLAlchemy):

    zone = create_zone()

    assert SecureZoneService.create(zone, 42) == Zone.query.get(1)


@patch.object(LocationService, "has_permission", lambda *args: True)
def test_delete_by_id(db: SQLAlchemy):

    z1: Zone = Zone(**create_zone())

    z2: Zone = Zone(**create_zone(zone_id=2))

    db.session.add(z1)
    db.session.add(z2)
    db.session.commit()

    event_id = SecureZoneService.delete_by_id(1, 12)

    res: List[Zone] = Zone.query.all()

    assert event_id == 1
    assert z1 not in res
    assert z2 in res
