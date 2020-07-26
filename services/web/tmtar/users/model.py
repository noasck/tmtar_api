from services.web.tmtar.project import db


class User(db.Model):
    '''User Widget describes fields related to basic auth and role accessing'''

    __tablename__ = 'users'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email_hash = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer, nullable=True)
    location_id = db.Column(db.Integer, nullable=True)
    sex = db.Column(db.Integer, nullable=True)
    role = db.Column(db.Integer, nullable=False, default=0)
    admin_location_id = db.Column(db.Integer, nullable=True)
