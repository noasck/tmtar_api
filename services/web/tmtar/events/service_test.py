from time import time
from typing import List
from unittest.mock import patch

import pytest
from flask_sqlalchemy import SQLAlchemy

from ..files.model import File
from ..project.types import EventType
from ..tests.fixtures import app, db  # noqa
from .interface import IEvent
from .model import Event
from .service import LocationAccessError, LocationService, SecureEventService

time_now = int(time())


@pytest.fixture
def sample_file(db: SQLAlchemy) -> File:
    sample_file = File(filename='sample.png')
    db.session.add(sample_file)
    db.session.commit()
    return sample_file


def create_event(
        event_type=EventType[0],
        location_id=1,
        update_date=time_now,
        title="Sample",
        short_description="""The plugin adds a random text generator, capable
                 of creating witty texts in different genres. Created text can be inserted newly at the caret,
                 or replace a selection.""",
        description=""" The plugin adds a random text generator, capable of
                 creating witty texts in different genres. Created text can be inserted newly at the caret,
                 or replace a selection. The plugin adds a random text generator, capable of creating witty
                 texts in different genres. Created text can be inserted newly at the caret, or replace a selection.""",
        image_file_name='sample.png',
        active=True,
) -> IEvent:
    return IEvent(
        event_type=event_type,
        location_id=location_id,
        update_date=update_date,
        title=title,
        short_description=short_description,
        description=description,
        image_file_name=image_file_name,
        active=active,
    )


@patch.object(LocationService, 'get_all_ancestors_id', lambda *args: [1, 2])
def test_get_events_by_user_location(db: SQLAlchemy, sample_file: File):
    """
    Cases:
    + Case 1: location_id is out of user available
    + Case 2: active = False
    + Case 3: event type is different
    """
    event_type_to_find = EventType[0]
    event_type_to_ignore = EventType[1]

    LocationService.create({"id": 2, "name": "loc1", "root": 1})
    LocationService.create({"id": 3, "name": "loc2", "root": 1})

    e1 = Event(**create_event(location_id=2, event_type=event_type_to_find))
    e2 = Event(**create_event(location_id=2, active=False))
    e3 = Event(**create_event(location_id=2, event_type=event_type_to_ignore))
    e4 = Event(**create_event(location_id=3))

    eg1 = Event(**create_event(location_id=1, event_type=event_type_to_find))
    eg2 = Event(**create_event(location_id=1, event_type=event_type_to_ignore))
    eg3 = Event(**create_event(location_id=1, active=False))

    db.session.add_all([e1, e2, e3, e4, eg1, eg2, eg3])
    db.session.commit()

    result = SecureEventService.get_by_user_location(
        event_type_to_find,
        1,
    )

    assert len(result) == 2
    assert result == [e1, eg1]

    db.session.add_all(
        [Event(**create_event(location_id=1, event_type=event_type_to_find)) for _ in range(10)]
    )

    result = SecureEventService.get_by_user_location(
        event_type_to_find,
        1,
    )
    assert len(result) == 10


class TestSecuredEventUpdate:
    """
        Testing update Event functionality.

        Cases:
        + Case 1: has access to location. No location_id update.
        - Case 2: has NO access to location. Exception.
        + Case 3: has access to location and updated location.
        - Case 4: has NO access to updated location. Exception.
        """

    @patch.object(LocationService, 'has_permission', lambda *args: True)
    def test_case1(self, db: SQLAlchemy, sample_file: File):
        event_upd = IEvent(active=True, title='Wubba Lubba')
        event = Event(**create_event(active=False))

        db.session.add(event)
        db.session.commit()

        SecureEventService.update(event, event_upd, 1)
        events = Event.query.all()

        assert len(events) == 1

        assert events[0].title == 'Wubba Lubba'

    @patch.object(LocationService, 'has_permission', lambda *args: False)
    def test_case2(self, db: SQLAlchemy, sample_file: File):
        event_upd = IEvent(active=True, title='Wubba Lubba')
        event = Event(**create_event(active=False))

        db.session.add(event)
        db.session.commit()

        try:
            SecureEventService.update(event, event_upd, 1)
        except LocationAccessError:
            assert True

    @patch.object(LocationService, 'has_permission', lambda *args: True)
    def test_case3(self, db: SQLAlchemy, sample_file: File):
        event_upd = IEvent(active=True, title='Wubba Lubba', location_id=2)
        event = Event(**create_event(active=False))

        LocationService.create({"id": 2, "name": "loc1", "root": 1})

        db.session.add(event)
        db.session.commit()

        SecureEventService.update(event, event_upd, 1)
        events = Event.query.all()

        assert len(events) == 1

        assert events[0].title == 'Wubba Lubba'

        assert events[0].location_id == 2

    # returns True for first check and False for second (see Service class).
    @patch.object(LocationService, 'has_permission', lambda l1, l2: l2 == 42)
    def test_case4(self, db: SQLAlchemy, sample_file: File):
        event_upd = IEvent(active=True, title='Wubba Lubba', location_id=2)
        event = Event(**create_event(active=False))

        LocationService.create({"id": 2, "name": "loc1", "root": 1})

        db.session.add(event)
        db.session.commit()

        try:
            SecureEventService.update(event, event_upd, 42)
        except LocationAccessError:
            assert True


@patch.object(LocationService, 'get_all_successor_id', lambda *args: [1, 2, 5])
def test_safe_get_all(db: SQLAlchemy, sample_file: File):
    event_type_to_find = EventType[0]
    event_type_to_ignore = EventType[1]

    LocationService.create({"id": 2, "name": "loc1", "root": 1})
    LocationService.create({"id": 3, "name": "loc2", "root": 1})

    e1 = Event(**create_event(location_id=2, event_type=event_type_to_find))
    e2 = Event(**create_event(location_id=2, active=False))
    e3 = Event(**create_event(location_id=2, event_type=event_type_to_ignore))
    e4 = Event(**create_event(location_id=3))

    eg1 = Event(**create_event(location_id=1, event_type=event_type_to_find))
    eg3 = Event(**create_event(location_id=1, active=False))
    eg2 = Event(**create_event(location_id=1, event_type=event_type_to_ignore))

    db.session.add_all([e1, e2, e3, e4, eg1, eg2, eg3])
    db.session.commit()

    result = SecureEventService.get_rw_accessible(
        event_type_to_find,
        1,
    )

    # check filters
    assert len(result) == 4
    for event in result:
        assert event in {e1, e2, eg1, eg3}

    # check pagination
    db.session.add_all(
        [Event(**create_event(location_id=1, event_type=event_type_to_find)) for _ in range(10)]
    )

    result = SecureEventService.get_rw_accessible(
        event_type_to_find,
        1,
    )
    assert len(result) == 10


@patch.object(LocationService, "has_permission", lambda *args: True)
def test_create(sample_file: File):

    event = create_event()

    assert SecureEventService.create(event, 42) == Event.query.get(1)


@patch.object(LocationService, "has_permission", lambda *args: True)
def test_delete_by_id(db: SQLAlchemy, sample_file: File):

    e1: Event = Event(**create_event())

    e2: Event = Event(**create_event())

    db.session.add(e1)
    db.session.add(e2)
    db.session.commit()

    event_id = SecureEventService.delete_by_id(1, 12)

    res: List[Event] = Event.query.all()

    assert event_id == 1
    assert e1 not in res
    assert e2 in res
