from ..tests.fixtures import *
from .model import File

from pytest import fixture


@fixture
def file() -> File:
    return File(filename='sample.ext')


def test_File_create(file: File):
    assert file
