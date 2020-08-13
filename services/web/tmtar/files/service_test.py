from ..tests.fixtures import db, app # noqa

from flask_sqlalchemy import SQLAlchemy
from typing import List
from .model import File
from .service import FileService


def test_get_all(db: SQLAlchemy):
    f1: File = File(id=1, filename='sample1.txt')
    f2: File = File(id=2, filename='sample2.txt')

    db.session.add(f1)
    db.session.add(f2)
    db.session.commit()

    results: List[File] = FileService.get_all()

    assert len(results) == 2
    assert all((f1 in results, f2 in results))


def test_delete_by_filename(db: SQLAlchemy):
    f1: File = File(id=1, filename='sample1.txt')
    f2: File = File(id=2, filename='sample2.txt')

    db.session.add(f1)
    db.session.add(f2)
    db.session.commit()

    FileService.delete_by_filename('sample1.txt')

    result = File.query.all()

    assert len(result) == 1
    assert f2 in result


def test_search_by_filename(db: SQLAlchemy):
    f1: File = File(id=1, filename='sample1.txt')
    f2: File = File(id=2, filename='sample2.txt')

    db.session.add(f1)
    db.session.add(f2)
    db.session.commit()

    res1: List[File] = FileService.search_by_filename('sample')
    res2: List[File] = FileService.search_by_filename('1')
    res3: List[File] = FileService.search_by_filename('ss')

    assert f1 in res1 and f2 in res1
    assert f1 in res2 and len(res2) == 1
    assert not res3
