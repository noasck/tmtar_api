from ..tests.fixtures import db, app
from flask_sqlalchemy import SQLAlchemy
from typing import List
from .model import User
from .service import UserService
from .interface import IUser
from .types import RoleType, SexType


def test_get_all(db: SQLAlchemy):
    admin: User = User(id=1, email_hash=str(hash('example1@mail.ex')), role=RoleType.ADMIN, sex=SexType.MALE, location_id=1, age=18, admin_location_id=0)
    u1: User = User(id=2, email_hash=str(hash('example2@mail.ex')), role=RoleType.COMMON, sex=SexType.MALE, location_id=1, age=20)
    u2: User = User(id=3, email_hash=str(hash('example3@mail.ex')), role=RoleType.COMMON, sex=SexType.FEMALE, location_id=2, age=45)

    db.session.add(admin)
    db.session.add(u1)
    db.session.add(u2)
    db.session.commit()

    results: List[User] = UserService.get_all()

    assert len(results) == 3
    assert all((admin in results, u1 in results, u2 in results))


def test_update(db: SQLAlchemy):
    u1: User = User(id=2, email_hash=str(hash('example1@mail.ex')), role=RoleType.COMMON, sex=SexType.MALE, location_id=1, age=20)
    db.session.add(u1)
    db.session.commit()

    upd: IUser = IUser(email_hash=str(hash('new_email@mail.ex')), age=111)
    UserService.update(u1, upd)

    result: User = UserService.get_by_id(u1.id)

    assert result.email_hash == str(hash('example1@mail.ex'))
    assert result.age == 111


def test_delete_by_id(db: SQLAlchemy):
    u1: User = User(id=2, email_hash=str(hash('example2@mail.ex')), role=RoleType.COMMON, sex=SexType.MALE, location_id=1, age=20)
    u2: User = User(id=3, email_hash=str(hash('example3@mail.ex')), role=RoleType.COMMON, sex=SexType.FEMALE, location_id=2, age=45)

    db.session.add(u1)
    db.session.add(u2)
    db.session.commit()

    UserService.delete_by_id(u1.id)

    result = User.query.all()

    assert len(result) == 1
    assert u2 in result


def test_create(db: SQLAlchemy):

    u1 = UserService.get_or_new_by_email('example3@mail.ex')
    u2 = UserService.get_or_new_by_email('example3@mail.ex')

    assert u1 == u2