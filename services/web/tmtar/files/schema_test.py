from pytest import fixture

from .model import File
from .schema import FileSchema


@fixture
def schema() -> FileSchema:
    return FileSchema()


def test_FileSchema_create(schema: FileSchema):  # noqa
    assert schema
