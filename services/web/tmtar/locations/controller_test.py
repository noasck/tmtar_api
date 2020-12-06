from unittest.mock import patch
from flask.testing import FlaskClient

from ..tests.fixtures import *  # noqa
from .service import LocationService
from .model import Location
from .schema import LocationSchema
from .interface import ILocation
from . import BASE_ROUTE


def make_location(
        location_id: int = 123, name: str = 'Test city', root: int = 0
) -> Location:
    return Location(id=location_id, name=name, root=root)


def make_update(loc: Location, loc_upd: ILocation) -> Location:
    new_loc = make_location(loc.id, loc_upd['name'], loc_upd['root'])
    return new_loc


class TestLocationResource:
    @patch.object(
        LocationService,
        "get_roots",
        lambda: [
            make_location(123, name='Test city 1'),
            make_location(234, 'Test city 2', 123)
        ]
    )
    def test_get(self, client: FlaskClient):
        with client:
            result = client.get(f"/api/{BASE_ROUTE}", follow_redirects=True).get_json()
            expected = (
                LocationSchema(many=True)
                .dump(
                    [
                        make_location(123, name='Test city 1'),
                        make_location(234, 'Test city 2', 123)
                    ]
                )
            )
            assert len(result) != 0
            for i in result:
                assert i in expected

    @patch.object(
        LocationService, "create", lambda create_request: Location(**create_request)
    )
    def test_post(self, client: FlaskClient, token: str):
        with client:
            payload = dict(name='Test city')
            result = client.post(f"/api/{BASE_ROUTE}/", json=payload,
                                 headers={"Authorization": f"Bearer {token}"}).get_json()
            expected = (
                LocationSchema().dump(
                    Location(name=payload["name"])
                )
            )
            assert result == expected


class TestLocationIdResource:
    @patch.object(LocationService, "get_by_id",
                  lambda location_id:
                  make_location(location_id, name='Test city 1'),
                  )
    def test_get(self, client: FlaskClient, token: str):
        with client:
            result = client.get(f"/api/{BASE_ROUTE}/123", follow_redirects=True,
                                headers={"Authorization": f"Bearer {token}"}).get_json()
            expected = (
                LocationSchema()
                .dump(
                    make_location(123, name='Test city 1'),
                )
            )
            assert result == expected

    @patch.object(LocationService, "get_children", lambda location_id: [make_location(123, 'test', location_id)])
    def test_get_children(self, client: FlaskClient):
        with client:
            result = client.get(f"/api/{BASE_ROUTE}/children/121").get_json()
            expected = (
                LocationSchema(many=True).dump(
                    [
                        make_location(location_id=123, name='test', root=121)
                    ]
                )
            )
            print(result)
            assert result == expected

    @patch.object(LocationService, "get_by_id", lambda location_id: make_location(location_id, 'test', 22))
    @patch.object(LocationService, "get_parent", lambda location: make_location(location.root, 'test', 11))
    def test_get_parent(self, client: FlaskClient):
        with client:
            result = client.get(f"/api/locations/parent/121").get_json()
            expected = (
                LocationSchema().dump(
                        make_location(location_id=22, name='test', root=11)
                )
            )
            assert result == expected

    @patch.object(LocationService, "delete_by_id", lambda location_id: location_id)
    def test_delete(self, client: FlaskClient, token: str):
        with client:
            result = client.delete(f"/api/{BASE_ROUTE}/123", headers={"Authorization": f"Bearer {token}"}).get_json()
            expected = dict(status="Success", id=123)
            assert result == expected

    @patch.object(LocationService, "get_by_id", lambda location_id: make_location(location_id=location_id))
    @patch.object(LocationService, "update", make_update)
    def test_put(self, client: FlaskClient, token: str):
        with client:
            result = client.put(
                f"/api/{BASE_ROUTE}/123",
                json={"name": "New city", "root": 122}, headers={"Authorization": f"Bearer {token}"}
            ).get_json()

            expected = (
                LocationSchema()
                .dump(make_location(location_id=123, name="New city", root=122))
            )

            assert result == expected


class TestLocationSearchResource:
    @patch.object(LocationService, "search_by_name",
                  lambda str_to_find: [make_location(location_id=1, name=str_to_find, root=2)])
    def test_get(self, client: FlaskClient):
        result = client.get(f"/api/{BASE_ROUTE}/search/Child Location").get_json()

        expected_locations = LocationSchema().dump([make_location(location_id=1, name="Child Location", root=2)],
                                                   many=True)

        expected = dict(status='Match', locations=expected_locations)
        assert result == expected
