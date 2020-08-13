from ..tests.fixtures import * # noqa
from flask_sqlalchemy import SQLAlchemy
from typing import List
from .model import User
from .service import UserService
from .interface import IUser
from ..project.types import RoleType, SexType
from datetime import datetime


def test_get_all(db: SQLAlchemy):
    admin: User = User(id=1, email_hash=str(hash('example1@mail.ex')), role=RoleType[1],
                       sex=SexType[0], location_id=1, bdate=datetime.now().date(), admin_location_id=0)
    u1: User = User(id=2, email_hash=str(hash('example2@mail.ex')), role=RoleType[0],
                    sex=SexType[1], location_id=1, bdate=datetime.now().date())
    u2: User = User(id=3, email_hash=str(hash('example3@mail.ex')), role=RoleType[0],
                    sex=SexType[0], location_id=2, bdate=datetime.now().date())

    db.session.add(admin)
    db.session.add(u1)
    db.session.add(u2)
    db.session.commit()

    results: List[User] = UserService.get_all()

    assert len(results) == 3
    assert all((admin in results, u1 in results, u2 in results))


def test_update(db: SQLAlchemy):
    u1: User = User(id=2, email_hash=str(hash('example1@mail.ex')), role=RoleType[0],
                    sex=SexType[1], location_id=1, bdate=datetime.now().date())
    db.session.add(u1)
    db.session.commit()

    upd: IUser = IUser(email_hash=str(hash('new_email@mail.ex')), bdate='2016-07-04', sex=SexType[1])
    UserService.update(u1, upd)

    result: User = UserService.get_by_id(u1.id)

    assert result.email_hash == str(hash('example1@mail.ex'))
    assert result.bdate == datetime.strptime('2016-07-04', '%Y-%m-%d').date()
    assert result.sex == SexType[1]


def test_delete_by_id(db: SQLAlchemy):
    u1: User = User(id=2, email_hash=str(hash('example2@mail.ex')), role=RoleType[0], sex=SexType[0],
                    location_id=1, bdate=datetime.now().date())
    u2: User = User(id=3, email_hash=str(hash('example3@mail.ex')), role=RoleType[0], sex=SexType[1],
                    location_id=2, bdate=datetime.now().date())

    db.session.add(u1)
    db.session.add(u2)
    db.session.commit()

    UserService.delete_by_id(u1.id)

    result = User.query.all()

    assert len(result) == 1
    assert u2 in result


def test_get_or_new():

    u1 = UserService.get_or_new_by_email('example3@mail.ex')
    u2 = UserService.get_or_new_by_email('example3@mail.ex')

    assert u1 == u2
