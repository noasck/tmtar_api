from ..tests.fixtures import * # noqa
from pytest import fixture

from .model import Object


@fixture
def new_object() -> Object:
    return Object(
        name="SampleName",
        target_image_file="jksdgf34778r8erg", # noqa
        asset_file="soidfhskjdnfksd", # noqa
        subzone_id=1
    )

def test_Object_create(new_object: Object): # noqa
    assert new_object
