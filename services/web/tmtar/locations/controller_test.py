from unittest.mock import patch
from flask.testing import FlaskClient

from ..tests.fixtures import client, app
from .service import LocationService
from .model import Location
from .schema import LocationSchema
from .interface import ILocation
from . import BASE_ROUTE


def make_location(
        id: int = 123, name: str = 'Test city', root: int = 0
) -> Location:
    return Location(id=id, name=name, root=root)


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
        for i in result:
            assert i in expected
