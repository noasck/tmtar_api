from unittest.mock import patch
from flask.testing import FlaskClient

from ..tests.fixtures import *  # noqa
from .service import ObjectService
from .model import Object
from .schema import ObjectSchema
from .interface import IObject
from . import BASE_ROUTE


def make_object(
        object_id: int = 12, name: str = 'Test object', target_image_file="some image",
        asset_file="asset file", subzone_id: int = 0
) -> Object:
    return Object(id=object_id, name=name, target_image_file=target_image_file,
                  asset_file=asset_file, subzone_id=subzone_id)


def make_update(obj: Object, obj_upd: IObject) -> Object:
    new_object = make_object(obj.id, obj_upd['name'], obj_upd['target_image_file'],
                             obj_upd['asset_file'], obj_upd['subzone_id'])
    return new_object


class TestObjectResource:
    @patch.object(
        ObjectService,
        "get_all",
        lambda: [
            make_object(3, 'Test object 1', "Image 1", "Asset file 5", 2),
            make_object(object_id=7, name='Test 2', target_image_file="Image 2")
        ]
    )
    def test_get(self, client: FlaskClient):
        with client:
            result = client.get(f"/api/{BASE_ROUTE}", follow_redirects=True).get_json()
            expected = (
                ObjectSchema(many=True)
                .dump(
                    [
                        make_object(3, 'Test object 1', "Image 1", "Asset file 5", 2),
                        make_object(object_id=7, name='Test 2', target_image_file="Image 2")
                    ]
                )
            )
            assert len(result) != 0
            for i in result:
                assert i in expected

    @patch.object(
        ObjectService, "create", lambda create_request: Object(**create_request)
    )
    def test_post(self, client: FlaskClient):
        with client:
            payload = dict(name="Sample Object")
            result = client.post(f"/api/{BASE_ROUTE}", json=payload).get_json()
            expected = (
                ObjectSchema().dump(
                    Object(name=payload['name'])
                )
            )
            assert result == expected


class TestObjectIdResource:
    @patch.object(ObjectService, "get_by_id",
                  lambda object_id: make_object(object_id, name="Test object 1",
                                                target_image_file="Image 1",
                                                subzone_id=4))
    def test_get(self, client: FlaskClient):
        with client:
            result = client.get(f"/api/{BASE_ROUTE}/7")
            expected = (
                ObjectSchema()
                .dump(
                    make_object(object_id=7, name='Test 2', target_image_file="Image 2")
                )
            )
            assert result in expected

    @patch.object(ObjectService, "get_by_id", lambda object_id: make_object(object_id=object_id))
    @patch.object(ObjectService, "update", make_update)
    def test_put(self, client: FlaskClient):
        with client:
            result = client.put(
                f"/api/{BASE_ROUTE}/7",
                json={"name": "Test object 1", "object_id": 7, "target_image_file": "Image 1"}
            ).get_json()

            excepted = (
                ObjectSchema()
                .dump(make_object(object_id=7, name="Test object 1", target_image_file="Image 1"))
            )
            assert result == excepted

    @patch.object(ObjectService, "delete_by_id",
                  lambda object_id: object_id)
    def test_delete(self, client: FlaskClient):
        with client:
            result = client.delete(f"/api/{BASE_ROUTE}/7").get_json()
            excepted = dict(status="Success", id=7)
        assert result == excepted


class TestObjectSubzoneIdResource:
    @patch.object(ObjectService, "get_by_subzone_id",
                  lambda subzone_id: make_object(name="Test 1", subzone_id=3))
    def test_get(self, client: FlaskClient):
        with client:
            result = client.get(f"/api/{BASE_ROUTE}/3")
            expected = (
                ObjectSchema(many=True).dump(
                    [
                        make_object(name='Test 1', subzone_id=3)
                    ]
                )
            )
            assert result in expected


class TestObjectSearchResource:
    @patch.object(ObjectService, "search_by_name",
                  lambda str_to_find: [make_object(object_id=3, name=str_to_find)])
    def test_get(self, client: FlaskClient):
        result = client.get(f"/api/{BASE_ROUTE}/search/Object 2").get_json()
        excepted_objects = ObjectSchema().dump([make_object(object_id=3, name="Object 2")], many=True)
        excepted = dict(status="Match", objects=excepted_objects)

        assert result == excepted
