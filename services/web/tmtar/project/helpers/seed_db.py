from ...users.model import User
from ...locations.service import Location

from ..injector import Injector


def seed_db():
    # TODO: encrypt field and hide in config
    db = Injector().db
    u1: User = User(id=228, email=str('denter425@gmail.com'),
                    location_id=1, admin_location_id=1)
    u2: User = User(id=1337, email=str('jjok730@gmail.com'),
                    location_id=1, admin_location_id=1)

    root_location = Location(id=1, root=None, name="root")

    db.session.add(u1)
    db.session.add(u2)
    db.session.add(root_location)
    db.session.commit()

    return [u1.email, u2.email]
