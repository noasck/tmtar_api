from ..project.injector import Injector
from .interface import IObject

db = Injector.db


class Object(db.Model):
    """
    Object model describes table with objects of augmented reality,
    containing asset files and describing parameters.
    """
    __tablename__ = 'objects'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    target_image_file = db.Column(db.String(255), nullable=False)
    asset_file = db.Column(db.String(255), nullable=False)
    subzone_id = db.Column(db.Integer, nullable=False, index=True)

    def update(self, changes: IObject):
        for key, val in changes.items():
            if key != 'id':
                setattr(self, key, val)
        return self
