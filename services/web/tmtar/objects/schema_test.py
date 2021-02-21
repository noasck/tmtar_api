from pytest import fixture

from .model import Object
from .interface import IObject
from .schema import ObjectSchema


@fixture
def schema() -> ObjectSchema:
    return ObjectSchema()

def test_ObjectSchema_create(schema: ObjectSchema): # noqa
    assert schema

def test_ObjectSchema_works(schema: ObjectSchema): # noqa
    params: IObject = schema.load(
        {
            'id': "1",
            'name': "SampleName",
            'target_image_file': "lorem_ipsum",
            'asset_file': "lorem_ipsum",
            'subzone_id': "1"
        }
    )

    object = Object(**params) # noqa
    assert object.id == 1
    assert object.name == "SampleName"
    assert object.target_image_file == "lorem_ipsum"
    assert object.asset_file == "lorem_ipsum"
    assert object.subzone_id == 1
