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
    def get_root(cls) -> Union[Location, None]:
        """
        Get seeded root Location.

        :return: root Location
        :rtype: Union[Location, None]
        """
        return Location.query.filter_by(name='root').first_or_404()

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
    def check_location_permission(
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
