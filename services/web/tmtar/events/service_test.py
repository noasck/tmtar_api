from ..tests.fixtures import db, app  # noqa
from unittest.mock import patch
from flask_sqlalchemy import SQLAlchemy
from typing import List

from .model import Event
from .service import EventService, LocationChecker
from .interface import IEvent
from ..project.types import EventType, SexType
from time import time

time_now = int(time())


@patch.object(LocationChecker, "check", lambda *args: True)
def test_create():
    event = IEvent(id=1, event_type=EventType[0], location_id=1, update_date=time_now, sex=SexType[0], min_age=12,
                   max_age=100, title="Sample", short_description="""The plugin adds a random text generator, capable 
                 of creating witty texts in different genres. Created text can be inserted newly at the caret, 
                 or replace a selection.""", description=""" The plugin adds a random text generator, capable of 
                 creating witty texts in different genres. Created text can be inserted newly at the caret, 
                 or replace a selection. The plugin adds a random text generator, capable of creating witty 
                 texts in different genres. Created text can be inserted newly at the caret, or replace a selection.""",
                   image_file_name='sample.png', active=True)

    assert EventService.create(event, 42) == Event.query.get(1)


@patch.object(LocationChecker, "check", lambda *args: True)
def test_delete_by_id(db: SQLAlchemy):
    e1: Event = Event(id=1, event_type=EventType[0], location_id=1, update_date=time_now, sex=SexType[0], min_age=12,
                      max_age=100, title="Sample", short_description="""The plugin adds a random text generator, capable 
                 of creating witty texts in different genres. Created text can be inserted newly at the caret, 
                 or replace a selection.""", description=""" The plugin adds a random text generator, capable of 
                 creating witty texts in different genres. Created text can be inserted newly at the caret, 
                 or replace a selection. The plugin adds a random text generator, capable of creating witty 
                 texts in different genres. Created text can be inserted newly at the caret, or replace a selection.""",
                      image_file_name='sample.png', active=True)

    e2: Event = Event(id=2, event_type=EventType[0], location_id=1, update_date=time_now, sex=SexType[0], min_age=12,
                      max_age=100, title="Sample", short_description="""The plugin adds a random text generator, capable 
                 of creating witty texts in different genres. Created text can be inserted newly at the caret, 
                 or replace a selection.""", description=""" The plugin adds a random text generator, capable of 
                 creating witty texts in different genres. Created text can be inserted newly at the caret, 
                 or replace a selection. The plugin adds a random text generator, capable of creating witty 
                 texts in different genres. Created text can be inserted newly at the caret, or replace a selection.""",
                      image_file_name='sample.png', active=True)

    db.session.add(e1)
    db.session.add(e2)
    db.session.commit()

    event_id = EventService.delete_by_id(1, 12)

    res: List[Event] = Event.query.all()

    assert event_id == [1]
    assert e1 not in res
    assert e2 in res


# @patch.object(LocationChecker, "check", lambda *args: True)
# def
#
#
#
#
# //////////////
#
# def test_get_all(db: SQLAlchemy):
#     uk, kh, kv = create_test_locations(db)
#
#     results: List[Location] = LocationService.get_all()
#
#     assert len(results) == 3
#     assert all((uk in results, kh in results, kv in results))
#
#
# def test_update(db: SQLAlchemy):
#     kv: Location = Location(id=3, name='kyiv')
#     db.session.add(kv)
#     db.session.commit()
#
#     upd: ILocation = ILocation(name='Kyiv')
#     LocationService.update(kv, upd)
#
#     result: Location = Location.query.get(kv.id)
#
#     assert result.name == 'Kyiv'
#
#
# def test_delete_by_id(db: SQLAlchemy):
#     kh: Location = Location(id=2, name='kherson', root=1)
#     kv: Location = Location(id=3, name='kyiv', root=1)
#
#     db.session.add(kh)
#     db.session.add(kv)
#     db.session.commit()
#
#     LocationService.delete_by_id(kh.id)
#
#     result = Location.query.all()
#
#     assert len(result) == 1
#     assert kv in result
#
#
# def test_get_parent(db: SQLAlchemy):
#     uk, kh, kv = create_test_locations(db)
#
#     assert LocationService.get_parent(kh) == LocationService.get_parent(kv) == uk
#     assert LocationService.get_parent(uk) is None
#
#
# def test_get_children(db: SQLAlchemy):
#     uk, kh, kv = create_test_locations(db)
#
#     nk = Location(id=4, name='nova каховка', root=3)
#
#     db.session.add(nk)
#     db.session.commit()
#
#     result: List[Location] = LocationService.get_children(uk.id)
#
#     assert len(result) == 2
#     assert kh in result and kv in result
#     assert len(LocationService.get_children(kh.id)) == 0
#     assert nk in LocationService.get_children(kv.id) and len(LocationService.get_children(kv.id)) == 1
#
#
# def test_get_roots(db: SQLAlchemy):
#     uk, kh, kv = create_test_locations(db)
#     nk = Location(id=4, name='nova каховка', root=3)
#     pk = Location(id=5, name='nova каховка')
#
#     db.session.add(nk)
#     db.session.add(pk)
#     db.session.commit()
#
#     result: List[Location] = LocationService.get_roots()
#
#     assert len(result) == 2
#     assert pk in result and uk in result
#
#
# def test_search_by_name(db: SQLAlchemy):
#     create_test_locations(db)
#     nk = Location(id=4, name='nova каховка', root=3)
#     pk = Location(id=5, name='NoVa Каховка')
#
#     db.session.add(nk)
#     db.session.add(pk)
#     db.session.commit()
#
#     res1: List[Location] = LocationService.search_by_name("k")
#     res2: List[Location] = LocationService.search_by_name("K")
#     res3: List[Location] = LocationService.search_by_name("nova")
#     res4: List[Location] = LocationService.search_by_name("kkk")
#
#     assert all(list(map(lambda x: x in res2, res1)))
#     assert len(res1) == 3
#     assert len(res3) == 2 and nk in res3 and pk in res3
#     assert len(res4) == 0
