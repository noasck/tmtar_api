from flask_sqlalchemy import SQLAlchemy
from geoalchemy2 import Geography
from sqlalchemy.orm import backref

from ..project.injector import Injector
from .constants import Constants
from .interface import IZone

db: SQLAlchemy = Injector.db


class Zone(db.Model):
    """Widget describes GIS PhotoZone object."""

    __tablename__ = 'zones'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String(Constants.title_max_length), nullable=False)
    description = db.Column(db.String(Constants.description_max_length), nullable=True)
    actual_address = db.Column(db.String, nullable=True)
    location_id = db.Column(
        db.Integer,
        db.ForeignKey('locations.id', ondelete='SET DEFAULT', onupdate='CASCADE'),
        server_default='1',
        nullable=False,
    )
    preview_image_filename = db.Column(
        db.String,
        db.ForeignKey('files.filename', ondelete='SET NULL', onupdate='CASCADE'),
        nullable=True,
    )
    center = db.Column(
        Geography(
            geometry_type='POINT',
            srid=Constants.SRID,
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
    preview_image = db.relationship(
        'File',
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
            setattr(self, key, new_value)
        return self
