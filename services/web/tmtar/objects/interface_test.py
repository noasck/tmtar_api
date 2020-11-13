from ..tests.fixtures import * # noqa
from pytest import fixture

from .model import Object
from .interface import IObject


@fixture
def interface() -> IObject:
    return IObject(
        name="SampleName",
        target_image_file="jksdgf34778r8erg", # noqa
        asset_file="soidfhskjdnfksd", # noqa
        subzone_id=1
    )


def test_IObject_create(interface: IObject): # noqa
    assert interface


def test_IObject_works(interface: IObject): # noqa
    new_object = Object(**interface) # noqa
    assert new_object
