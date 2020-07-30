from ..project import FlaskApp
from .types import RoleType, SexType
from .interface import IUser
db = FlaskApp.Instance().database


class User(db.Model):
    '''User Widget describes fields related to basic auth and role accessing'''

    __tablename__ = 'users'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email_hash = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer, nullable=True)
    location_id = db.Column(db.Integer, nullable=True)
    sex = db.Column(db.Enum(SexType), nullable=True)
    role = db.Column(db.Enum(RoleType), nullable=False, default=0)
    admin_location_id = db.Column(db.Integer, nullable=True)

    def update(self, changes: IUser):
        for key, val in changes.items():
            if key != 'id' and key != 'email_hash':
                setattr(self, key, val)
        return self