from ..tests.fixtures import db, app
from flask_sqlalchemy import SQLAlchemy
from typing import List
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

    upd: ILocation = ILocation(name='Kyiv')
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

    assert LocationService.get_parent(kh) == LocationService.get_parent(kv) == uk
    assert LocationService.get_parent(uk) is None


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


def test_get_roots(db: SQLAlchemy):
    uk: Location = Location(id=1, name='ukraine', root=0)
    kh: Location = Location(id=2, name='kherson', root=1)
    kv: Location = Location(id=3, name='kyiv', root=1)
    nk = Location(id=4, name='nova каховка', root=3)
    pk = Location(id=5, name='nova каховка')

    db.session.add(uk)
    db.session.add(kh)
    db.session.add(kv)
    db.session.add(nk)
    db.session.add(pk)
    db.session.commit()

    result: List[Location] = LocationService.get_roots()

    assert len(result) == 2
    assert pk in result and uk in result


def test_search_by_name(db: SQLAlchemy):
    uk: Location = Location(id=1, name='ukraine', root=0)
    kh: Location = Location(id=2, name='kherson', root=1)
    kv: Location = Location(id=3, name='kyiv', root=1)
    nk = Location(id=4, name='nova каховка', root=3)
    pk = Location(id=5, name='NoVa Каховка')

    db.session.add(uk)
    db.session.add(kh)
    db.session.add(kv)
    db.session.add(nk)
    db.session.add(pk)
    db.session.commit()

    res1: List[Location] = LocationService.search_by_name("k")
    res2: List[Location] = LocationService.search_by_name("K")
    res3: List[Location] = LocationService.search_by_name("nova")
    res4: List[Location] = LocationService.search_by_name("kkk")

    assert all(list(map(lambda x: x in res2, res1)))
    assert len(res1) == 3
    assert len(res3) == 2 and nk in res3 and pk in res3
    assert len(res4) == 0
