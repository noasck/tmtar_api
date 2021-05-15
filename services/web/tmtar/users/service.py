from typing import Optional

from ..project.abstract.abstract_service import AbstractService
from .interface import IUser
from .model import User


class UserService(AbstractService[User, IUser]):
    """Class implements Location db operations."""

    @classmethod
    def model(cls):
        """
        Resolve Location model class.

        :return: Location Type.
        :rtype: type
        """
        return User

    @classmethod
    def get_by_identity(cls, identity: str) -> Optional[User]:
        """
        Get certain User by identity.

        :param identity: user's identity
        :type identity: str
        :return: matched user
        :rtype: str
        """
        return User.query.filter_by(identity=identity).first()

    @classmethod
    def get_or_new_by_identity(cls, identity: str):
        """
        Get existing or create new User by received identity.

        :param identity: logged in users identity
        :type identity: str
        :return: User instance
        :rtype: str
        """
        usr = UserService.get_by_identity(identity)
        if not usr:
            usr = User(identity=identity)
            cls._db.session.add(usr)
            cls._db.session.commit()
        return usr
