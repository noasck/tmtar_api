from time import time

from pytest import fixture

from ..project.types import *
from ..tests.fixtures import *  # noqa
from .interface import IEvent
from .model import Event
from .schema import EventSchema, UpdateEventSchema

time_now = str(int(time()))


@fixture
def schema() -> EventSchema:
    return EventSchema()


def test_schema_create(schema: EventSchema):
    assert schema


def test_schema_works(schema: EventSchema):
    params: IEvent = schema.load(
        dict(
            id='1',
            event_type=EventType[0],
            location_id='1',
            update_date=time_now,
            title="Sample",
            short_description="""The plugin adds a random text generator, capable 
                     of creating witty texts in different genres. Created text can be inserted newly at the caret, 
                     or replace a selection.""",
            description=""" The plugin adds a random text generator, capable of 
                     creating witty texts in different genres. Created text can be inserted newly at the caret, 
                     or replace a selection. The plugin adds a random text generator, capable of creating witty 
                     texts in different genres. 
                     Created text can be inserted newly at the caret, or replace a selection.""",
            image_file_name='sample.png',
            active='True'))

    event: Event = Event(**params)

    assert event.id == 1
    assert event.event_type == EventType[0]
    assert event.location_id == 1
    assert event.update_date == int(time_now)
    assert event.title == "Sample"
    assert event.short_description == """The plugin adds a random text generator, capable 
                     of creating witty texts in different genres. Created text can be inserted newly at the caret, 
                     or replace a selection."""
    assert event.description == """ The plugin adds a random text generator, capable of 
                     creating witty texts in different genres. Created text can be inserted newly at the caret, 
                     or replace a selection. The plugin adds a random text generator, capable of creating witty 
                     texts in different genres. 
                     Created text can be inserted newly at the caret, or replace a selection."""
    assert event.image_file_name == 'sample.png'
    assert event.active


def test_update_schema_works():
    params: IEvent = UpdateEventSchema().load(
        dict(
            id='1',
            event_type=EventType[0],
            location_id='1',
            update_date=time_now,
            title="Sample",
            short_description="""The plugin adds a random text generator, capable 
                     of creating witty texts in different genres. Created text can be inserted newly at the caret, 
                     or replace a selection.""",
            description=""" The plugin adds a random text generator, capable of 
                     creating witty texts in different genres. Created text can be inserted newly at the caret, 
                     or replace a selection. The plugin adds a random text generator, capable of creating witty 
                     texts in different genres. 
                     Created text can be inserted newly at the caret, or replace a selection.""",
            image_file_name='sample.png',
            active='True')
    )

    event: Event = Event(**params)

    assert event.id == 1
    assert event.event_type == EventType[0]
    assert event.location_id == 1
    assert event.update_date == int(time_now)
    assert event.title == "Sample"
    assert event.short_description == """The plugin adds a random text generator, capable 
                     of creating witty texts in different genres. Created text can be inserted newly at the caret, 
                     or replace a selection."""
    assert event.description == """ The plugin adds a random text generator, capable of 
                     creating witty texts in different genres. Created text can be inserted newly at the caret, 
                     or replace a selection. The plugin adds a random text generator, capable of creating witty 
                     texts in different genres. 
                     Created text can be inserted newly at the caret, or replace a selection."""
    assert event.image_file_name == 'sample.png'
    assert event.active
