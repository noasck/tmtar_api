from typing import List

from ..project.abstract.abstract_service import AbstractService
from ..project.injector import Injector
from .interface import IFile
from .model import File

db = Injector.db


class FileService(AbstractService[File, IFile]):
    """Class implements File db operations."""

    @classmethod
    def model(cls):
        """
        Resolve File model class.

        :return: File Type.
        :rtype: type
        """
        return File

    @classmethod
    def delete_by_filename(cls, filename: str) -> List[int]:
        """Delete specific File by filename."""
        file_instance = cls.model().query.filter_by(
            filename=filename,
        ).first_or_404()
        cls._db.session.delete(file_instance)
        cls._db.session.commit()
        return file_instance

    @classmethod
    def search_by_filename(cls, str_to_search: str) -> List[File] or None:
        """Search specific File by substring of filename."""
        return File.query.filter(
            File.filename.ilike(f'%{str_to_search}%'),
        ).all()
