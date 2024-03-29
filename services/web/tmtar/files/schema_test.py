from pytest import fixture

from .model import File
from .schema import FileSchema


@fixture
def schema() -> FileSchema:
    return FileSchema()


def test_FileSchema_create(schema: FileSchema):  # noqa
    assert schema


def test_FileSchema_works(schema: FileSchema):  # noqa
    params = schema.load({'filename': 'testfile.txt'})
    widget = File(**params)

    assert widget.filename == 'testfile.txt'
