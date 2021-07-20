from flask_sqlalchemy import SQLAlchemy
from geoalchemy2 import Geography
from sqlalchemy.orm import backref

from ..project.injector import Injector
from .interface import IZone

db: SQLAlchemy = Injector.db
SRID = 4326


class Zone(db.Model):
    """Widget describes GIS PhotoZone object."""

    __tablename__ = 'zones'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String, nullable=False)
    location_id = db.Column(
        db.Integer,
        db.ForeignKey('locations.id', ondelete='CASCADE', onupdate='CASCADE'),
        nullable=False,
    )

    center = db.Column(
        Geography(
            geometry_type='POINT',
            srid=SRID,
        ),
        index=True,
        nullable=False,
    )

    radius = db.Column(
        db.Float,
        nullable=False,
    )
    active = db.Column(
        db.Boolean,
        nullable=False,
        default=True,
    )
    secret = db.Column(
        db.Boolean,
        nullable=False,
        default=False,
    )

    location = db.relationship(
        'Location',
        backref=backref(
            'zones',
            passive_deletes='all',
            lazy='select',
        ),
        lazy='noload',
    )

    def update(self, changes: IZone):
        """Update certain record."""
        for key, new_value in changes.items():
            if key != 'id':
                setattr(self, key, new_value)
        return self
