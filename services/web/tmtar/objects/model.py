from ..project.injector import Injector
from .interface import IObject

db = Injector.db


class Object(db.Model):
    """Objects of augmented reality, containing asset files."""

    __tablename__ = 'objects'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    target_image_file = db.Column(db.String(255), nullable=False)
    asset_file = db.Column(db.String(255), nullable=False)
    subzone_id = db.Column(db.Integer, nullable=False, index=True)

    def update(self, changes: IObject):
        """Update certain record."""
        for key, new_value in changes.items():
            setattr(self, key, new_value)
        return self
