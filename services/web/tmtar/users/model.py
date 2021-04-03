from ..project.injector import Injector
from .interface import IUser

db = Injector.db


class User(db.Model):
    """Widget describes fields related to basic auth and role accessing."""

    __tablename__ = 'users'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String, nullable=False)
    bdate = db.Column(db.Date, nullable=True)
    location_id = db.Column(db.Integer, nullable=True)
    sex = db.Column(db.String, nullable=True)
    admin_location_id = db.Column(db.Integer, nullable=True)

    def update(self, changes: IUser):
        """Update certain record."""
        for key, new_value in changes.items():
            if key not in {'id', 'email'}:
                setattr(self, key, new_value)
        return self
