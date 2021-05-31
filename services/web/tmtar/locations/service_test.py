from typing import List

from flask_sqlalchemy import SQLAlchemy

from ..tests.fixtures import app, db  # noqa
from .interface import ILocation
from .model import Location
from .service import LocationService


def create_test_locations(db):
    uk: Location = Location(id=2, name='ukraine', root=1)
    kh: Location = Location(id=3, name='kherson', root=2)
    kv: Location = Location(id=4, name='kyiv', root=2)

    db.session.add(uk)
    db.session.add(kh)
    db.session.add(kv)
    db.session.commit()

    return uk, kh, kv


def test_get_all(db: SQLAlchemy):
    uk, kh, kv = create_test_locations(db)

    results: List[Location] = LocationService.get_all()

    assert len(results) == 4
    assert all((uk in results, kh in results, kv in results))


def test_update(db: SQLAlchemy):
    kv: Location = Location(id=3, name='kyiv', root=1)
    db.session.add(kv)
    db.session.commit()

    upd: ILocation = ILocation(name='Kyiv')
    LocationService.update(kv, upd)

    result: Location = Location.query.get(kv.id)

    assert result.name == 'Kyiv'


def test_delete_by_id(db: SQLAlchemy):
    kh: Location = Location(id=2, name='kherson', root=1)
    kv: Location = Location(id=3, name='kyiv', root=2)
    kl: Location = Location(id=5, name='steek', root=1)
    pv: Location = Location(id=4, name='peek', root=3)

    db.session.add(kh)
    db.session.add(kv)
    db.session.add(kl)
    db.session.add(pv)
    db.session.commit()

    LocationService.delete_by_id(kh.id)

    result = Location.query.all()

    assert len(result) == 2
    assert kl in result


def test_get_parent(db: SQLAlchemy):
    uk, kh, kv = create_test_locations(db)

    assert LocationService.get_parent(kh) == LocationService.get_parent(
        kv) == uk
    assert LocationService.get_parent(uk).name == "root"


def test_get_children_works(db: SQLAlchemy):
    uk, kh, kv = create_test_locations(db)

    nk = Location(id=5, name='nova каховка', root=4)

    db.session.add(nk)
    db.session.commit()

    result: List[Location] = LocationService.get_children(uk)

    assert len(result) == 2
    assert kh in result and kv in result
    assert len(LocationService.get_children(kh)) == 0
    assert nk in LocationService.get_children(kv) and len(
        LocationService.get_children(kv)) == 1


def test_get_root(db: SQLAlchemy):
    uk, kh, kv = create_test_locations(db)
    nk = Location(id=5, name='nova каховка', root=4)
    pk = Location(id=6, name='nova кахо вка', root=None)

    db.session.add(nk)
    db.session.add(pk)
    db.session.commit()

    result: Location = LocationService.get_root()

    assert result.name == "root"


def test_search_by_name(db: SQLAlchemy):
    create_test_locations(db)
    nk = Location(id=5, name='nova каховка', root=4)
    pk = Location(id=6, name='NoVa Каховка')

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


def test_create(db: SQLAlchemy):
    new_loc: ILocation = {"name": "Simple", "root": 1, "id": 2}

    loc = LocationService.create(new_loc)
    assert loc.id != 0
    assert loc
