# Event
# - id : int
# - update_date : int
# - event_type : str
# - location_id : int
# - sex : str
# - min_age : int
# - max_age : int
# - name : str
# - title : str
# - short_desc : str
# - decription : str
# - image : str
# - active : bool

from ..injectors.app import FlaskApp
from time import time
# from .interface import ILocation

db = FlaskApp.Instance().database


class Event(db.Model):
    '''Event Widget contain news and sales'''

    __tablename__ = 'users'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    event_type = db.Column(db.String(255), nullable=False, index=True)
    location_id = db.Column(db.Integer, nullable=False)
    update_date = db.Column(db.Integer, onupdate=int(time()))
