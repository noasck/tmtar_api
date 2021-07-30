from flask_sqlalchemy import SQLAlchemy

from ...locations.model import Location
from ...users.model import User
from ..fixtures import *


def test_user_location_relation(db: SQLAlchemy):
    loc1 = Location(id=2, name='sample1', root=1)
    loc2 = Location(id=3, name='sample2', root=1)

    u1 = User(identity='sample_user_1', location_id=2, admin_location_id=2)
    u2 = User(identity='sample_user_1', location_id=3)

    db.session.add(loc1)
    db.session.add(loc2)

    db.session.add(u1)
    db.session.add(u2)

    db.session.commit()

    db.session.delete(loc1)
    db.session.commit()

    users = User.query.all()

    assert len(users) == 4
    assert u2 in users and u1 in users
    assert u1.location_id == 1
    assert u2.location_id == 3
    assert u1.admin_location_id is None
