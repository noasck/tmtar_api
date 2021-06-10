from http import HTTPStatus
from typing import List

from flask_restx import abort

from ..project.abstract.abstract_service import AbstractService
from ..project.exceptions import LocationAccessError
from ..project.injector import Injector
from .interface import IEvent
from .model import Event

LocationService = Injector.LocationService


class _EventService(AbstractService[Event, IEvent]):
    @classmethod
    def model(cls):
        """
        Resolve Location model class.
        :return: Location Type.
        :rtype: type
        """
        return Event


class SecureEventService(object):
    """Implements protected by location hierarchy service over EventService"""

    # TODO: on request: inverse propagation of the events from parents to children.
    @classmethod
    def get_by_user_location(
        cls,
        event_type,
        user_location_id,
        page: int = 1,
    ) -> List[Event]:
        """
        Get matching news by user private info.

        :param event_type: 'news' or 'sales' accepted
        :type event_type: str
        :param user_location_id: location id from User instance
        :type user_location_id: int
        :param page: pagination page number
        :type page: int
        :return: List of matching events
        :rtype: List[Event]
        """
        per_page = 10
        appropriated_locations = LocationService.get_all_ancestors_id(
            user_location_id,
        )

        events = Event.query.filter(
            Event.location_id.in_(appropriated_locations),
            Event.active == True,
            Event.event_type == event_type
        ).order_by(Event.update_date.desc()).paginate(page, per_page, error_out=False).items

        return events

    @classmethod
    def update(
        cls,
        event: Event,
        event_upd: IEvent,
        user_admin_location_id: int,
    ) -> Event:
        """
        Safely update specific event with dict.

        :param event: event to update.
        :type event: Event
        :param event_upd: new fields
        :type event_upd: IEvent
        :param user_admin_location_id: [0] user db admin location id.
        :type user_admin_location_id: int
        :return: updated event.
        :rtype: Event
        :raises LocationAccessError: if user don't have necessary permissions.
        """
        if not LocationService.has_permission(event.location_id, user_admin_location_id):
            raise LocationAccessError(
                error="You don't have permissions to access this location!",
                status_code=HTTPStatus.FORBIDDEN,
            )

        if 'location_id' in event_upd.keys():
            if not LocationService.has_permission(event_upd['location_id'], user_admin_location_id):
                raise LocationAccessError(
                    error="You don't have permissions to access this location!",
                    status_code=HTTPStatus.FORBIDDEN,
                )

        return _EventService.update(event, event_upd)

    @classmethod
    def get_rw_accessible(
        cls,
        event_type,
        user_admin_location_id,
        page: int = 1,
    ):
        """
        Get all accessible events for certain admin location id.

        :param event_type: 'news' or 'sales' accepted
        :type event_type: str
        :param user_admin_location_id: admin location id from User instance.
        :type user_admin_location_id: int
        :param page: pagination page number.
        :type page: int
        :return: List of matching events.
        :rtype: List[Event]
        """
        per_page = 10
        appropriated_locations = LocationService.get_all_successor_id(
            user_admin_location_id,
        )

        events = Event.query.filter(
            Event.location_id.in_(appropriated_locations),
            Event.event_type == event_type
        ).order_by(Event.update_date.desc()).paginate(page, per_page, error_out=False).items

        return events

    @classmethod
    def create(
        cls,
        new_event: IEvent,
        user_admin_location_id: int,
    ) -> Event:
        """
        Safely create event with dict.

        :param new_event: fields for new event.
        :type new_event: IEvent
        :param user_admin_location_id: [0] user db admin location id.
        :type user_admin_location_id: int
        :return: updated event.
        :rtype: Event
        :raises LocationAccessError: if user don't have necessary permissions.
        """
        try:
            if not LocationService.has_permission(new_event['location_id'], user_admin_location_id):
                raise LocationAccessError(
                    error="You don't have permissions to access this location!",
                    status_code=HTTPStatus.FORBIDDEN,
                )
        except KeyError:
            abort(HTTPStatus.BAD_REQUEST, message='New Event location id is not specified.')

        return _EventService.create(new_event)

    @classmethod
    def delete_by_id(
        cls,
        event_id: int,
        user_admin_location_id: int,
    ) -> int:
        """
        Safely update specific event with dict.

        :param event_id: db id of Event to delete.
        :type event_id: IEvent
        :param user_admin_location_id: [0] user db admin location id.
        :type user_admin_location_id: int
        :return: updated event.
        :rtype: Event
        :raises LocationAccessError: if user don't have necessary permissions.
        """
        try:
            if not LocationService.has_permission(
                _EventService.get_by_id(event_id).location_id,
                user_admin_location_id,
            ):
                raise LocationAccessError(
                    error="You don't have permissions to access this location!",
                    status_code=HTTPStatus.FORBIDDEN,
                )
        except KeyError:
            abort(HTTPStatus.BAD_REQUEST, message='New Event location id is not specified.')

        return _EventService.delete_by_id(event_id)
