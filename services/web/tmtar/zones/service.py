from http import HTTPStatus

from flask_restx import abort

from ..project.abstract.abstract_service import AbstractService
from ..project.exceptions import LocationAccessError
from ..project.injector import Injector
from .interface import IZone
from .model import Zone

LocationService = Injector.LocationService


class _ZoneService(AbstractService[Zone, IZone]):
    @classmethod
    def model(cls):
        """
        Resolve Zone model class.

        :return: Location Type.
        :rtype: type
        """
        return Zone


# TODO: add clone method

class SecureZoneService(object):
    """Implements protected by location hierarchy service over ZoneService."""

    @classmethod
    def update_by_id(
        cls,
        zone_id: int,
        zone_upd: IZone,
        user_admin_location_id: int,
    ) -> Zone:
        """
        Safely update specific zone by id with dict.

        :param zone_id: zone db id to update.
        :type zone_id: int
        :param zone_upd: new fields
        :type zone_upd: IZone
        :param user_admin_location_id: [0] user db admin location id.
        :type user_admin_location_id: int
        :return: updated zone.
        :rtype: Zone
        :raises LocationAccessError: if user don't have necessary permissions.
        """
        zone = _ZoneService.get_by_id(zone_id)

        if not LocationService.has_permission(zone.location_id, user_admin_location_id):
            raise LocationAccessError()

        if 'location_id' in zone_upd.keys():
            if not LocationService.has_permission(zone_upd['location_id'], user_admin_location_id):
                raise LocationAccessError()

        return _ZoneService.update(zone, zone_upd)

    @classmethod
    def get_by_location_id(
        cls,
        user_admin_location_id,
    ):
        """
        Get all accessible zones for certain admin location id.

        :param user_admin_location_id: admin location id from User instance.
        :type user_admin_location_id: int
        :return: List of matching zones.
        :rtype: List[Zone]
        """
        appropriated_locations = LocationService.get_all_successor_id(
            user_admin_location_id,
        )

        return Zone.query.filter(Zone.location_id.in_(appropriated_locations)).all()

    @classmethod
    def create(
        cls,
        new_zone: IZone,
        user_admin_location_id: int,
    ) -> Zone:
        """
        Safely create zone with dict.

        :param new_zone: fields for new zone.
        :type new_zone: IZone
        :param user_admin_location_id: [0] user db admin location id.
        :type user_admin_location_id: int
        :return: updated zone.
        :rtype: Zone
        :raises LocationAccessError: if user don't have necessary permissions.
        """
        try:
            if not LocationService.has_permission(new_zone['location_id'], user_admin_location_id):
                raise LocationAccessError()
        except KeyError:
            abort(HTTPStatus.BAD_REQUEST, message='New Zone location_id is not specified.')

        return _ZoneService.create(new_zone)

    @classmethod
    def delete_by_id(
        cls,
        zone_id: int,
        user_admin_location_id: int,
    ) -> int:
        """
        Safely update specific zone with dict.

        :param zone_id: db id of zone to delete.
        :type zone_id: int
        :param user_admin_location_id: [0] user db admin location id.
        :type user_admin_location_id: int
        :return: updated zone.
        :rtype: int
        :raises LocationAccessError: if user don't have necessary permissions.
        """
        has_permission = LocationService.has_permission(
            _ZoneService.get_by_id(zone_id).location_id,
            user_admin_location_id,
        )

        if not has_permission:
            raise LocationAccessError()

        return _ZoneService.delete_by_id(zone_id)
