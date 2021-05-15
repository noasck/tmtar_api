from abc import ABC, abstractmethod
from typing import Callable

from flask import Flask

from ..builders.singleton import singleton


class AbstractIdentityLoader(ABC):
    """
    Abstract class providing interface for identity and auth handling.
    """

    @abstractmethod
    def __init__(self, app: Flask):
        """
        Read envs from config.
        """
        pass

    @singleton("verify_token")
    def get_verifier(self) -> Callable:
        """Inject verify_identity method."""
        return self.verify_identity

    @abstractmethod
    def verify_identity(self, token) -> str:
        """
        Check provided identity to be valid and return identity value.
        :return: main identifier.
        :rtype: str
        """
        pass
