from typing import List, Union

from ..project.abstract.abstract_service import AbstractService
from .interface import ILocation
from .model import Location


class LocationService(AbstractService[Location, ILocation]):
    """Class implements Location db operations."""

    @classmethod
    def model(cls):
        """
        Resolve Location model class.

        :return: Location Type.
        :rtype: type
        """
        return Location

    @classmethod
    def get_parent(cls, child: Location) -> Union[Location, None]:
        """
        Get root of the Location instance.

        :param child: current node.
        :type child: Location
        :return: Root location of current instance.
        :rtype: Union[Location, None]
        """
        return child.parent

    @classmethod
    def get_all_ancestors_id(cls, location_id: int) -> List[int]:
        """
        Get all parent's ids of the Location instance.

        :param location_id: certain node Location id.
        :type location_id: int
        :return: List of all ancestors ids for current location.
        :rtype: List[int]
        """
        # TODO: adjust to LTree realization
        node = cls.get_by_id(location_id)
        if node is not None:
            ids = [node.id]
            current = node.parent
            while current is not None:
                ids.append(current.id)
                current = current.parent
            return ids
        return []

    @classmethod
    def get_all_successor_id(
        cls,
        location_id: int,
    ) -> List[int]:
        """
        Get all child's ids of the Location instance.

        :param location_id: certain node Location id.
        :type location_id: int
        :return: List of all successors' ids for current location.
        :rtype: List[int]
        """
        node = cls.get_by_id(location_id)
        queue = [node]
        successors_ids = []
        while queue:
            child: Location = queue.pop()
            child_children: List[Location] = child.children
            if child_children:
                queue.extend(child_children)
            successors_ids.append(child.id)
        return successors_ids

    @classmethod
    def search_by_name(cls, str_to_search: str) -> Union[List[Location], None]:
        """
        Find Locations with matching substring of name.

        :param str_to_search: substring - case insensitive.
        :type str_to_search: str
        :return: list of matching Locations or None.
        :rtype: Union[List[Location], None]
        """
        return Location.query.filter(
            Location.name.ilike(f'%{str_to_search}%'),
        ).all()

    @classmethod
    def get_children(cls, parent: Location) -> List[Location]:
        """
        Get all children of certain Location instance.

        :param parent: current instance
        :type parent: Location
        :return: children of current instance
        :rtype: List[Location]
        """
        return parent.children

    @classmethod
    def has_permission(
        cls,
        location_id: int,
        accessed_location_id: int,
    ) -> bool:
        """
        Check permissions of user by location.

        :param location_id: id of user rbac location.
        :type location_id: int
        :param accessed_location_id: Location of required object.
        :type accessed_location_id: int
        :return: if user have permission to access.
        :rtype: bool
        """
        loc = LocationService.get_by_id(location_id)
        has_access = False
        if accessed_location_id == 0:
            return True
        while loc is not None:
            if loc.id == accessed_location_id:
                has_access = True
            loc = LocationService.get_parent(loc)
        return has_access
