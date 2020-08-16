from ..injectors.app import FlaskApp
from ..project.types import RoleType, SexType # noqa
from .interface import IUser
db = FlaskApp.Instance().database


class User(db.Model):
    """User Widget describes fields related to basic auth and role accessing"""

    __tablename__ = 'users'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email_hash = db.Column(db.String(255), nullable=False)
    bdate = db.Column(db.Date, nullable=True)
    location_id = db.Column(db.Integer, nullable=True)
    sex = db.Column(db.String, nullable=True)
    role = db.Column(db.String, nullable=False, default="")
    admin_location_id = db.Column(db.Integer, nullable=True)

    def update(self, changes: IUser):
        for key, val in changes.items():
            if key != 'id' and key != 'email_hash':
                setattr(self, key, val)
        return self
