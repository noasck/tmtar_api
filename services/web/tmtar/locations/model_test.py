from ..tests.fixtures import * # noqa
from pytest import fixture
from .model import Location


@fixture
def location() -> Location:
    return Location(
        name="Sample name"
    )


def test_Location_create(location: Location): # noqa
    assert location
