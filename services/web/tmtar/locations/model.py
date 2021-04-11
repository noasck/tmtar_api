from ..project.injector import Injector
from .interface import ILocation

db = Injector.db


class Location(db.Model):
    """Include and describe geographic objects and their relations."""

    __tablename__ = 'locations'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String, nullable=False)
    root = db.Column(
        db.Integer,
        db.ForeignKey('locations.id', onupdate='CASCADE', ondelete='CASCADE'),
        nullable=True,
    )
    children = db.relationship(
        'Location',
        backref=db.backref('parent', remote_side=[id]),
    )

    def update(self, changes: ILocation):
        """Update certain record."""
        for key, new_value in changes.items():
            setattr(self, key, new_value)
        return self
