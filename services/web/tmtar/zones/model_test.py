from geoalchemy2 import func
from pytest import fixture

from ..tests.fixtures import *
from .model import Zone


@fixture
def zone() -> Zone:
    return Zone(
        id=1,
        title="Abstract title",
        location_id=1,
        active=True,
        radius=123,
        center=func.ST_MakePoint(3.546456, 45.6567456),
        preview_image_filename="sdfsdf.sdf",
        description='sdfgdfgdfgdfgdfg',
        actual_address='sdfsdfsdf'
    )


def test_Zone_create(zone: Zone):
    assert zone