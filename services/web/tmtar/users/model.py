from ..project.injector import Injector
from .constants import SEX_FIELD_LENGTH
from .interface import IUser

db = Injector.db


class User(db.Model):
    """Widget describes fields related to basic auth and role accessing."""

    __tablename__ = 'users'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    identity = db.Column(db.String, nullable=False)
    bdate = db.Column(db.Date, nullable=True)
    location_id = db.Column(
        db.Integer,
        db.ForeignKey('locations.id', onupdate='CASCADE', ondelete='SET DEFAULT'),
        server_default='1',
        nullable=False,
    )
    sex = db.Column(db.String(SEX_FIELD_LENGTH), nullable=True)
    admin_location_id = db.Column(
        db.Integer,
        db.ForeignKey('locations.id', onupdate='CASCADE', ondelete='SET NULL'),
        nullable=True,
    )

    # Relations
    location = db.relationship(
        'Location',
        foreign_keys=[location_id],
        back_populates='users',
        lazy='noload',
    )
    admin_location = db.relationship(
        'Location',
        foreign_keys=[admin_location_id],
        back_populates='admins',
        lazy='noload',
    )

    def update(self, changes: IUser):
        """Update certain record."""
        for key, new_value in changes.items():
            setattr(self, key, new_value)
        return self
