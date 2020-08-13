from typing import List
from .model import File
from ..injectors.app import FlaskApp
import random
import string

db = FlaskApp.Instance().database


class AliasGenerator:
    """Generates alias for filename"""

    @staticmethod
    def random_string_generator(str_size: int = 40, allowed_chars=string.ascii_letters) -> str:
        """ returns a random string for file alias"""
        return ''.join(random.choice(allowed_chars) for _ in range(str_size))


class FileService:
    @staticmethod
    def get_all() -> List[File]:
        return File.query.all()

    @staticmethod
    def get_by_id(file_id: int) -> File:
        return File.query.get_or_404(file_id)

    @staticmethod
    def delete_by_filename(filename: str) -> List[int]:
        loc = File.query.filter_by(filename=filename).first_or_404()
        if not loc:
            return []
        file_id = loc.id
        db.session.delete(loc)
        db.session.commit()
        return [file_id]

    @staticmethod
    def search_by_filename(str_to_search: str) -> List[File] or None:
        files = FileService.get_all()

        def lower(x: str) -> str:
            return x.lower()

        return [city for city in files if lower(city.filename).find(lower(str_to_search)) != -1]

    @staticmethod
    def create(filename: str):
        file = File(filename=filename)
        db.session.add(file)
        db.session.commit()
        return file
