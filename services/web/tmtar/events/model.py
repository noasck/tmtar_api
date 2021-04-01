from ..project.injector import Injector
from time import time
from ..project.types import SexType
from .interface import IEvent

db = Injector().db


class Event(db.Model):
    """Event Widget contain news and sales"""

    __tablename__ = 'events'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    event_type = db.Column(db.String(255), nullable=False, index=True)
    location_id = db.Column(db.Integer, nullable=False)
    update_date = db.Column(db.Integer, onupdate=int(time()))
    sex = db.Column(db.String, default=SexType[3])
    min_age = db.Column(db.Integer, default=0)
    max_age = db.Column(db.Integer, default=150)
    title = db.Column(db.String, nullable=False)
    short_description = db.Column(db.Text, nullable=True)
    description = db.Column(db.Text, nullable=True)
    image_file_name = db.Column(db.String, nullable=True)
    active = db.Column(db.Boolean, default=True, nullable=False, index=True)

    def update(self, changes: IEvent):
        for key, val in changes.items():
            setattr(self, key, val)
        return self
