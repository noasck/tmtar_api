from time import time

from sqlalchemy import Column

from ..project.injector import Injector
from ..project.types import SexType
from .interface import IEvent

db = Injector.db


class Event(db.Model):
    """Event Widget contain news and sales."""

    __tablename__ = 'events'
    id: Column = db.Column(db.Integer, autoincrement=True, primary_key=True)
    event_type: Column = db.Column(db.String(255), nullable=False, index=True)
    location_id: Column = db.Column(
        db.Integer,
        db.ForeignKey('locations.id', onupdate='CASCADE', ondelete='CASCADE'),
        default=1,
        nullable=False,
    )
    update_date = db.Column(db.Integer, onupdate=int(time()), index=True)
    title = db.Column(db.String, nullable=False)
    short_description = db.Column(db.String(200), nullable=True)
    description = db.Column(db.Text, nullable=True)
    image_file_name = db.Column(
        db.String,
        db.ForeignKey('files.filename', onupdate='CASCADE', ondelete='CASCADE'),
        nullable=True,
    )
    active = db.Column(db.Boolean, default=True, nullable=False, index=True)

    def update(self, changes: IEvent):
        """Update certain record."""
        for key, new_value in changes.items():
            setattr(self, key, new_value)
        return self
