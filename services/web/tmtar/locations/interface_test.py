from ..tests.fixtures import *
from pytest import fixture
from .model import Location
from .interface import ILocation


@fixture
def interface() -> ILocation:
    return ILocation(id=1, name="test city", root=0)


def test_ILocation_create(interface: ILocation):
    assert interface


def test_ILocation_works(interface: ILocation):
    location = Location(**interface)
    assert location
