from typing import List

from flask_sqlalchemy import SQLAlchemy
from pytest import fixture

from ..tests.fixtures import app, db  # noqa
from .interface import IObject
from .model import Object
from .service import ObjectService


@fixture
def create_sample_objects(db: SQLAlchemy):
    o1 = Object(id=1,
                name="SampleName",
                target_image_file="lorem_ipsum",
                asset_file="lorem_ipsum",
                subzone_id=1)

    o2 = Object(id=2,
                name="name",
                target_image_file="lorem_ipsum",
                asset_file="lorem_ipsum",
                subzone_id=1)

    o3 = Object(id=3,
                name="SampleName2",
                target_image_file="lorem_ipsum",
                asset_file="lorem_ipsum",
                subzone_id=2)

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


def test_get_by_id(create_sample_objects: List[Object]):
    o1, o2, o3 = create_sample_objects

    assert ObjectService.get_by_id(1) == o1
    assert ObjectService.get_by_id(2) == o2
    assert ObjectService.get_by_id(3) == o3


def test_get_by_subzone_id(create_sample_objects: List[Object]):
    o1, o2, o3 = create_sample_objects

    res1: List[Object] = ObjectService.get_by_subzone_id(1)
    res2: List[Object] = ObjectService.get_by_subzone_id(2)

    assert len(res1) == 2
    assert len(res2) == 1
    assert o1 in res1 and o2 in res1
    assert o3 in res2


def test_search_by_name(create_sample_objects: List[Object]):
    o1, o2, o3 = create_sample_objects

    res1: List[Object] = ObjectService.search_by_name("Name")
    res2: List[Object] = ObjectService.search_by_name("N")
    res3: List[Object] = ObjectService.search_by_name("aa")

    assert len(res1) == 3 and o1 in res1 and o2 in res1 and o3 in res1
    assert len(res2) == 3
    assert not res3


def test_delete_by_id(create_sample_objects: List[Object]):
    o1, o2, o3 = create_sample_objects

    ind = ObjectService.delete_by_id(2)  # noqa

    result = ObjectService.get_all()

    assert len(result) == 2
    assert o1 in result and o3 in result


def test_create(db: SQLAlchemy):  # noqa
    new_object: IObject = {
        "name": "SampleName2",
        "target_image_file": "lorem_ipsum",
        "asset_file": "lorem_ipsum",
        "subzone_id": 2
    }

    obj = ObjectService.create(new_object)

    assert obj.id != 0
    assert obj.name == "SampleName2"
    assert obj.subzone_id == 2
    assert obj.asset_file == new_object['asset_file']
    assert obj.target_image_file == new_object['target_image_file']


def test_update(db: SQLAlchemy):
    obj: Object = Object(id=5,
                         name="Sample name",
                         subzone_id=4,
                         asset_file="File 4",
                         target_image_file="Some File 3")
    db.session.add(obj)
    db.session.commit()

    upd_obj: IObject = IObject(name="Sample name 3",
                               asset_file="Another asset file")
    ObjectService.update(obj, upd_obj)

    result: Object = Object.query.get(obj.id)

    assert result.name == 'Sample name 3'
    assert result.asset_file == 'Another asset file'
