from typing import List

from ..project.injector import Injector
from .interface import IObject
from .model import Object

# from ..injectors.accessor import LocationChecker
# from flask_restx import abort

db = Injector.db


class ObjectService:
    """ Service of object instance. """

    @staticmethod
    def get_all() -> List[Object]:
        """
        Get all objects.
        @return: list of all existing objects.
        """
        return Object.query.all()

    @staticmethod
    def get_by_id(object_id: int) -> Object:
        """
        Get single Object instance by id.
        @param object_id: valid id of Object table.
        @return: Object instance or 404.
        """
        return Object.query.get_or_404(object_id)

    @staticmethod
    def get_by_subzone_id(subzone_id: int) -> List[Object] or None:
        """
        Get objects located on specific subzone.
        @param subzone_id: Subzone db id.
        @return: list of objects in subzone.
        """
        return Object.query.filter_by(subzone_id=subzone_id).all()

    @staticmethod
    def search_by_name(str_to_search: str) -> List[Object] or None:
        """
        Finds all matching objects by part of name.
        @param str_to_search: part of name (case insensitive).
        @return: list of all alike objects.
        """
        return Object.query.filter(
            Object.name.ilike(f"%{str_to_search}%")).all()

    @staticmethod
    def update(object_to_update: Object, object_updates: IObject) -> Object:
        """
        Updates distinct object.
        @param object_to_update: object to retain new values.
        @param object_updates: interface with new values
        @return: updated_object
        """
        object_to_update.update(object_updates)
        db.session.commit()
        return object_to_update

    @staticmethod
    def create(new_object: IObject) -> Object:
        """
        Creates new Object instance in db.
        @param new_object: dict of input parameters to create object.
        @return: created Object in dv
        """
        obj = Object(name=new_object['name'],
                     target_image_file=new_object['target_image_file'],
                     asset_file=new_object['asset_file'],
                     subzone_id=new_object['subzone_id'])
        db.session.add(obj)
        db.session.commit()

        return obj

    @staticmethod
    def delete_by_id(object_id: int) -> List[int]:
        """
        Deletes Object from database by id.
        @param object_id: db Object id.
        @return: list of deleted object's ids.
        """
        obj = ObjectService.get_by_id(object_id)
        if not obj:
            return []
        db.session.delete(obj)
        db.session.commit()
        return [object_id]
