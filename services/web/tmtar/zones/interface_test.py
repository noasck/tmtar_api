from geoalchemy2 import func
from pytest import fixture

from .interface import IZone
from .model import Zone


@fixture
def interface() -> IZone:
    return IZone(
        id=1,
        title="Abstract title",
        location_id=1,
        active=True,
        radius=123,
        center=func.ST_MakePoint(3.546456, 45.6567456),
    )


def test_IZone_create(interface: IZone):
    assert interface


def test_IZone_works(interface: IZone):
    location = Zone(**interface)
    assert location
