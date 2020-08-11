from ..tests.fixtures import *
from pytest import fixture
from .model import Location


@fixture
def location() -> Location:
    return Location(
        name="Sample name"
    )


def test_Location_create(location: Location):
    assert location
