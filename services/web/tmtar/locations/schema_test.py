from pytest import fixture

from .interface import ILocation
from .model import Location
from .schema import LocationSchema, LocationUpdateSchema


@fixture
def schema() -> LocationSchema:
    return LocationSchema()


@fixture
def update_schema() -> LocationUpdateSchema:
    return LocationUpdateSchema()


def test_LocationSchema_create(schema: LocationSchema):  # noqa
    assert schema


def test_LocationSchema_works(schema: LocationSchema):  # noqa
    params: ILocation = schema.load({
        'name': 'test city',
        'root': '1'
    })
    widget = Location(**params)

    assert widget.name == 'test city'
    assert widget.root == 1


def test_LocationUpdateSchema_create(   # noqa
        update_schema: LocationUpdateSchema):  # noqa
    assert update_schema


def test_LocationUpdateSchema_works(update_schema: LocationUpdateSchema):  # noqa
    params: ILocation = update_schema.load({'name': 'test city'})
    widget = Location(**params)

    assert widget.name == 'test city'
