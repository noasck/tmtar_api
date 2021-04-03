from datetime import date
from typing import List

from ..project.abstract.abstract_service import AbstractService
from ..project.injector import Injector
from .interface import IEvent
from .model import Event

LocationService = Injector.LocationService


class EventService(AbstractService[Event, IEvent]):
    @classmethod
    def model(cls):
        """
        Resolve Location model class.
        :return: Location Type.
        :rtype: type
        """
        return Event


    @classmethod
    def get_specified(
        cls,
        event_type,
        user_location_id,
        bdate: date = date(1960, 12, 20),
        page: int = 1,
        sex: str = "all",
    ) -> List[Event]:
        """
        Get matching news by user private info.
        :param event_type: 'news' or 'sales' accepted
        :type event_type: str
        :param user_location_id: location id from User instance
        :type user_location_id: int
        :param bdate: birth date of user
        :type bdate: date
        :param page: future pagination source
        :type page: int
        :param sex: user sex 'male' or 'female'
        :type sex: str
        :return: List of matching events
        :rtype: List[Event]
        """
        per_page = 10

        def calculate_age(born):
            today = date.today()
            return today.year - born.year - ((today.month, today.day) <
                                             (born.month, born.day))

        age = calculate_age(bdate)

        def is_matching(event: Event):
            return (True if sex == "all" else event.sex == sex) and (event.max_age >= age >= event.min_age) \
                   and (LocationService.check_location_permission(event.location_id, user_location_id)
                        if user_location_id is not None else True) and event.active

        events = Event.query.order_by(Event.update_date.desc()).filter(
            Event.event_type == event_type).all()

        return [event for event in events if is_matching(event)]

    @staticmethod
    def update(event: Event, event_upd: IEvent,
               user_location_id) -> Event or None:
        if LocationService.check_location_permission(event.event_type, user_location_id) \
                and LocationService.check_location_permission(event_upd['location_id'], user_location_id):
            event.update(event_upd)
            db.session.commit()
            return event

    @staticmethod
    def delete_by_id(event_id: int, user_location_id: int) -> List[int]:
        event = Event.query.filter_by(id=event_id).first_or_404()
        if not event:
            return []
        if LocationService.check_location_permission(event.location_id,
                                                     user_location_id):
            db.session.delete(event)
            db.session.commit()
            return [event_id]
        else:
            return []

    @staticmethod
    def create(new_event: IEvent, user_location_id: int) -> Event or None:
        if LocationService.check_location_permission(new_event['location_id'],
                                                     user_location_id):
            event = Event(**new_event)
            db.session.add(event)
            db.session.commit()

            return event
        else:
            return None
