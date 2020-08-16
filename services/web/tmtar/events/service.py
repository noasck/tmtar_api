from typing import List
from .model import Event
from ..injectors.app import FlaskApp
from ..injectors.accessor import LocationChecker
from .interface import IEvent
from datetime import date


db = FlaskApp.Instance().database


class EventService:
    @staticmethod
    def get_all() -> List[Event]:
        return Event.query.all()

    @staticmethod
    def get_by_id(location_id: int) -> Event:
        return Event.query.get_or_404(location_id)

    @staticmethod
    def get_specified(event_type, user_location_id, bdate: date = date(1960, 20, 20),
                      page: int = 1, sex: str = "all") -> List[Event]: # noqa
        """
        Method responsible for getting matching news by user private info.
        @param event_type: 'news' or 'sales' accepted
        @param user_location_id: location id from User instance
        @param bdate: birth date of user
        @param page: future pagination source
        @param sex: user sex 'male' or 'female'
        @return: List of matching events
        """
        per_page = 10 # noqa

        def calculate_age(born):
            today = date.today()
            return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

        age = calculate_age(bdate)

        def is_matching(event: Event):
            return (True if sex == "all" else event.sex == sex) and (event.max_age >= age >= event.min_age) \
                   and LocationChecker.check(event.location_id, user_location_id) \
                   if user_location_id is not None else True

        events = Event.query.order_by(Event.update_date.desc()).filter(Event.event_type == event_type).all()

        return [event for event in events if is_matching(event)]

    @staticmethod
    def update(event: Event, event_upd: IEvent, user_location_id) -> Event or None:
        if LocationChecker.check(event.event_type, user_location_id)\
                and LocationChecker.check(event_upd['location_id'], user_location_id):
            event.update(event_upd)
            db.session.commit()
            return event

    @staticmethod
    def delete_by_id(event_id: int, user_location_id: int) -> List[int]:
        event = Event.query.filter_by(id=event_id).first_or_404()
        if not event:
            return []
        if LocationChecker.check(event['location_id'], user_location_id):
            db.session.delete(event)
            db.session.commit()
            return [event_id]
        else:
            return []

    @staticmethod
    def create(new_event: IEvent, user_location_id: int) -> Event or None:
        if LocationChecker.check(new_event['location_id'], user_location_id):
            event = Event(**new_event)
            db.session.add(event)
            db.session.commit()

            return event
        else:
            return None
