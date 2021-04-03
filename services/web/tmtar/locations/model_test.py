from pytest import fixture

from ..tests.fixtures import *  # noqa
from .model import Location


@fixture
def location() -> Location:
    return Location(name="Sample name")


def test_Location_create(location: Location):  # noqa
    assert location
