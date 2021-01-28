from pytest import fixture

from .model import Location
from .schema import LocationSchema, LocationUpdateSchema
from .interface import ILocation


@fixture
def schema() -> LocationSchema:
    return LocationSchema()


def test_LocationSchema_create(schema: LocationSchema): # noqa
    assert schema


def test_LocationSchema_works(schema: LocationSchema): # noqa
    params: ILocation = schema.load(
        {
            'id': '123',
            'name': 'test city',
            'root': '1'
        }
    )
    widget = Location(**params)

    assert widget.id == 123
    assert widget.name == 'test city'
    assert widget.root == 1


def test_LocationUpdateSchema_create(schema: LocationUpdateSchema): # noqa
    assert schema


def test_LocationUpdateSchema(schema: LocationUpdateSchema): # noqa
    params:  ILocation = schema.load(
        {
            'id': '12',
            'name': 'test city'
        }
    )
    widget = Location(**params)

    assert widget.id == 12
    assert widget.name == 'test city'
