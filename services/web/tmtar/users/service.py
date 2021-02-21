from typing import List, Optional

from .interface import IUser
from .model import User
from ..project.injector import Injector

db = Injector().db


class UserService:
    @staticmethod
    def get_all() -> List[User]:
        return User.query.all()

    @staticmethod
    def get_by_id(user_id: int) -> User:
        return User.query.get_or_404(user_id)

    @staticmethod
    def get_by_email(email: str) -> Optional[User]:
        return User.query.filter_by(email=email).first()

    @staticmethod
    def update(loc: User, loc_upd: IUser):
        loc.update(loc_upd)
        db.session.commit()
        return loc

    @staticmethod
    def delete_by_id(user_id: int) -> List[int]:
        loc = User.query.filter_by(id=user_id).first_or_404()
        if not loc:
            return []
        db.session.delete(loc)
        db.session.commit()
        return [user_id]

    @staticmethod
    def get_or_new_by_email(email: str):
        usr = UserService.get_by_email(email)
        if not usr:
            usr = User(email=email)
            db.session.add(usr)
            db.session.commit()
        return usr
