import binascii
import hashlib
import os
from typing import List, Optional

from .interface import IUser
from .model import User
from ..injectors.app import FlaskApp
from ..project.types import RoleType

db = FlaskApp.Instance().database


class UserService:
    @staticmethod
    def get_all() -> List[User]:
        return User.query.all()

    @staticmethod
    def get_by_id(user_id: int) -> User:
        return User.query.get_or_404(user_id)

    @staticmethod
    def get_by_email(email: str) -> Optional[User]:
        for user in UserService.get_all():
            if verify_email(user.email_hash, email):
                return user
        return None

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
    def get_or_new_by_email(email: str, role=RoleType[0]):
        usr = UserService.get_by_email(email)
        if not usr:
            usr = User(email_hash=hash_email(email), role=role)
            db.session.add(usr)
            db.session.commit()
        return usr


def hash_email(password):
    """Hash a password for storing."""
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwd_hash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),
                                   salt, 100000)
    pwd_hash = binascii.hexlify(pwd_hash)
    return (salt + pwd_hash).decode('ascii')


def verify_email(stored_password, provided_password):
    """Verify a stored password against one provided by user"""
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwd_hash = hashlib.pbkdf2_hmac('sha512',
                                   provided_password.encode('utf-8'),
                                   salt.encode('ascii'),
                                   100000)
    pwd_hash = binascii.hexlify(pwd_hash).decode('ascii')
    return pwd_hash == stored_password
