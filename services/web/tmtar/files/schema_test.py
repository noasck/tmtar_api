from pytest import fixture

from .model import File
from .schema import FileSchema

@fixture
def schema() -> FileSchema:
    return FileSchema()


def test_FileSchema_create(schema: FileSchema):
    assert schema


def test_FileSchema_works(schema: FileSchema):
    params = schema.load(
        {
            'id': 1,
            'filename': 'testfile.txt'
        }
    )
    widget = File(**params)

    assert widget.id == 1
    assert widget.filename == 'testfile.txt'
