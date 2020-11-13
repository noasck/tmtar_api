from ..tests.fixtures import db, app # noqa
from flask_sqlalchemy import SQLAlchemy
from typing import List
from .model import Object
from .service import ObjectService
from .interface import IObject
from pytest import fixture


@fixture
def create_sample_objects(db: SQLAlchemy):
    o1 = Object(
        id=1,
        name="SampleName",
        target_image_file="lorem_ipsum",
        asset_file="lorem_ipsum",
        subzone_id=1
    )

    o2 = Object(
        id=2,
        name="SampleName2",
        target_image_file="lorem_ipsum",
        asset_file="lorem_ipsum",
        subzone_id=1
    )

    o3 = Object(
        id=3,
        name="SampleName",
        target_image_file="lorem_ipsum",
        asset_file="lorem_ipsum",
        subzone_id=2
    )

    db.session.add(o1)
    db.session.add(o2)
    db.session.add(o3)
    db.session.commit()

    return [o1, o2, o3]


def test_get_all(create_sample_objects: List[Object]):
    o1, o2, o3 = create_sample_objects

    result = ObjectService.get_all()

    assert len(result) == 3
    assert all((o1 in result, o2 in result, o3 in result))

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
#
#
# def test_create(db: SQLAlchemy):
#     new_loc: ILocation = {
#         "name": "Simple",
#         "root": 0
#     }
#
#     loc = LocationService.create(new_loc)
#     assert loc.id != 0
#     assert loc
