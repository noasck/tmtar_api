from ..injectors.app import FlaskApp
from .interface import ILocation

db = FlaskApp.Instance().database


class Location(db.Model):
    """Location Widget describes table
    that includes geographic objects and their relations"""

    __tablename__ = 'locations'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    root = db.Column(db.Integer, default=0)

    def update(self, changes: ILocation):
        for key, val in changes.items():
            setattr(self, key, val)
        return self
