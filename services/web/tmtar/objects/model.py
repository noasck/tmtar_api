from ..injectors.app import FlaskApp

db = FlaskApp.Instance().database


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
