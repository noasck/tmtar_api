from typing import List
from .model import User
from ..project.types import RoleType
from ..injectors.app import FlaskApp
from .interface import IUser

db = FlaskApp.Instance().database


class UserService:
    @staticmethod
    def get_all() -> List[User]:
        return User.query.all()

    @staticmethod
    def get_by_id(id: int) -> User:
        return User.query.get_or_404(id)

    @staticmethod
    def get_by_email(email: str) -> User:
        return User.query.filter_by(email_hash=str(hash(email))).one_or_none()

    @staticmethod
    def update(loc: User, loc_upd: IUser):
        loc.update(loc_upd)
        db.session.commit()
        return loc

    @staticmethod
    def delete_by_id(id: int) -> List[int]:
        loc = User.query.filter_by(id=id).first_or_404()
        if not loc:
            return []
        db.session.delete(loc)
        db.session.commit()
        return [id]

    @staticmethod
    def get_or_new_by_email(email: str, role: RoleType = RoleType.COMMON):
        usr = UserService.get_by_email(email)
        if not usr:
            usr = User(email_hash=str(hash(email)), role=role)
            db.session.add(usr)
            db.session.commit()
        return usr
