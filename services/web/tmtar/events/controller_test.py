from unittest.mock import patch

from flask.testing import FlaskClient

from ..project.types import *
from ..tests.fixtures import *  # noqa
from . import BASE_ROUTE
from .interface import IEvent
from .model import Event
from .schema import EventSchema
from .service import SecureEventService


def create_event(
        event_id=1,
        event_type=EventType[0],
        location_id=1,
        update_date=123,
        title="Sample",
        short_description="""The plugin adds a random text generator, capable
                 of creating witty texts in different genres. Created text can be inserted newly at the caret,
                 or replace a selection.""",
        description=""" The plugin adds a random text generator, capable of
                 creating witty texts in different genres. Created text can be inserted newly at the caret,
                 or replace a selection. The plugin adds a random text generator, capable of creating witty
                 texts in different genres. Created text can be inserted newly at the caret, or replace a selection.""",
        image_file_name='sample.png',
        active=True,
        *args,
        **kwargs
) -> Event:
    return Event(
        id=event_id,
        event_type=event_type,
        location_id=location_id,
        update_date=update_date,
        title=title,
        short_description=short_description,
        description=description,
        image_file_name=image_file_name,
        active=active,
    )


def make_update(event_id, event_upd: IEvent, *args, **kwargs):
    return create_event(
        event_id=event_id,
        title = event_upd['title']
    )


class TestEventsResource:
    @patch.object(SecureEventService, 'create', lambda fields, *args, **kwargs: create_event(**fields))
    def test_post(self, client: FlaskClient, token: str):
        with client:
            payload = dict(title="Sample1", short_description="sjdnfsjdnffnsdf")
            result = client.post(f'/api/{BASE_ROUTE}/',
                                 json=payload,
                                 headers={
                                     "Authorization": f"Bearer {token}"
                                 }).get_json()

            expected = EventSchema().dump(create_event(**payload))

            assert result == expected


class TestPaginatedEventsSalesAndNewsResource:
    """
    Lets test all of that: all events getter, sales pagination, news pagination.
    """
    @patch.object(SecureEventService, 'get_all', lambda *args, **kwargs: [
        create_event(event_type=1),
        create_event(event_type=2),
    ])
    @patch.object(SecureEventService, 'get_by_user_location', lambda *args, **kwargs: [
        create_event(event_type=1),
        create_event(event_type=2),
    ])
    def test_get(self, client: FlaskClient, token: str):
        with client:
            def get_events_by_type(event_type: str):
                return client.get(
                    f'/api/{BASE_ROUTE}/{event_type}/1',
                    headers={
                        "Authorization": f"Bearer {token}"
                    }).get_json()

            expected = EventSchema(many=True).dump(
                [
                    create_event(event_type=1),
                    create_event(event_type=2),
                ]
            )
            result_all = get_events_by_type("all")
            result_sales = get_events_by_type("sales")
            result_news = get_events_by_type("news")

            assert result_all == expected
            assert result_sales == expected
            assert result_news == expected


class TestPaginatedEventsResource():
    """Events instance id resource."""

    @patch.object(SecureEventService, 'update_by_id', make_update)
    def test_put(self, client: FlaskClient, token: str):
        """Update single Event."""
        with client:
            result = client.put(
                f'/api/{BASE_ROUTE}/1',
                json={
                    'title': 'sample_new_title'
                },
                headers={
                    "Authorization": f"Bearer {token}"
                }
           ).get_json()
            expected = EventSchema().dump(create_event(title='sample_new_title'))
            assert result == expected

    @patch.object(SecureEventService, 'delete_by_id', lambda event_id, *args, **kwargs: event_id)
    def test_delete(self, client: FlaskClient, token: str):
        with client:
            result = client.delete(
                f'/api/{BASE_ROUTE}/1',
                headers={
                    "Authorization": f"Bearer {token}"
                }
            ).get_json()

        assert result == {'id': 1, 'status': 'Success'}


class TestEventsSearchResource():
    @patch.object(SecureEventService, 'search_by_title', lambda *args, **kwargs: [
        create_event(event_type=1),
        create_event(event_type=2),
    ])
    def test_get(self, client: FlaskClient, token: str):
        with client:
            def get_events_by_type(event_type: str):
                return client.get(
                    f'/api/{BASE_ROUTE}/{event_type}/search/dfgdfg',
                    headers={
                        "Authorization": f"Bearer {token}"
                    }).get_json()

            expected = {
                "status": "Match",
                "events":
                EventSchema(many=True).dump(
                [
                    create_event(event_type=1),
                    create_event(event_type=2),
                ]
            )}
            result_all = get_events_by_type("all")

            assert result_all == expected


class TestEventsCountResource():
    @patch.object(SecureEventService, 'count_all_events', lambda *args, **kwargs: 4)
    def test_get(self, client: FlaskClient, token: str):
        with client:
            def get_events_by_type(event_type: str):
                return client.get(
                    f'/api/{BASE_ROUTE}/{event_type}/count',
                    headers={
                        "Authorization": f"Bearer {token}"
                    }).get_json()

            expected = {
                "count": 4,
                }
            result_all = get_events_by_type("all")

            assert result_all == expected
