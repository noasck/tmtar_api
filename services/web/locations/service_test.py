from flask_sqlalchemy import SQLAlchemy
from typing import List
from ..tests.fixtures import db, app
from .model import Location
from .service import LocationService
from .interface import ILocation


def test_get_all(db: SQLAlchemy):
    uk: Location = Location(id=1, name='ukraine', root=0)
    kh: Location = Location(id=2, name='kherson', root=1)
    kv: Location = Location(id=3, name='kyiv', root=1)

    db.session.add(uk)
    db.session.add(kh)
    db.session.add(kv)
    db.session.commit()

    results: List[Location] = LocationService.get_all()

    assert len(results) == 3
    assert all((uk in results, kh in results, kv in results))


def test_update(db: SQLAlchemy):
    kv: Location = Location(id=3, name='kyiv')
    db.session.add(kv)
    db.session.commit()

    upd: ILocation = dict(name='Kyiv')
    LocationService.update(kv, upd)

    result: Location = Location.query.get(kv.id)

    assert result.name == 'Kyiv'


def test_delete_by_id(db: SQLAlchemy):
    kh: Location = Location(id=2, name='kherson', root=1)
    kv: Location = Location(id=3, name='kyiv', root=1)

    db.session.add(kh)
    db.session.add(kv)
    db.session.commit()

    LocationService.delete_by_id(kh.id)

    result = Location.query.all()

    assert len(result) == 1
    assert kv in result


def test_get_parent(db: SQLAlchemy):
    uk: Location = Location(id=1, name='ukraine', root=0)
    kh: Location = Location(id=2, name='kherson', root=1)
    kv: Location = Location(id=3, name='kyiv', root=1)

    db.session.add(uk)
    db.session.add(kh)
    db.session.add(kv)
    db.session.commit()

    assert LocationService.get_parent(kh.id) == LocationService.get_parent(kv.id) == uk
    assert LocationService.get_parent(uk.id) is None


def test_get_children(db: SQLAlchemy):
    uk: Location = Location(id=1, name='ukraine', root=0)
    kh: Location = Location(id=2, name='kherson', root=1)
    kv: Location = Location(id=3, name='kyiv', root=1)

    # nk = LocationService.create(
    #     ILocation(name='nova каховка', root=2)
    # )
    nk = Location(id=4, name='nova каховка', root=3)

    db.session.add(uk)
    db.session.add(kh)
    db.session.add(kv)
    db.session.add(nk)
    db.session.commit()

    result: List[Location] = LocationService.get_children(uk.id)

    assert len(result) == 2
    assert kh in result and kv in result
    assert len(LocationService.get_children(kh.id)) == 0
    assert nk in LocationService.get_children(kv.id) and len(LocationService.get_children(kv.id)) == 1



















