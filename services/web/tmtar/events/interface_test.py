import time
from datetime import datetime

from pytest import fixture

from ..project.types import EventType, SexType
from ..tests.fixtures import *  # noqa
from .interface import IEvent
from .model import Event

time_now = int(time.time())


@fixture
def interface() -> IEvent:
    return IEvent(
        id=1,
        event_type=EventType[0],
        location_id=1,
        update_date=datetime.utcnow(),
        title="Sample",
        short_description="""The plugin adds a random text generator, capable 
                 of creating witty texts in different genres. Created text can be inserted newly at the caret, 
                 or replace a selection.""",
        description=""" The plugin adds a random text generator, capable of 
                 creating witty texts in different genres. Created text can be inserted newly at the caret, 
                 or replace a selection. The plugin adds a random text generator, capable of creating witty 
                 texts in different genres. Created text can be inserted newly at the caret, or replace a selection.""",
        image_file_name='sample.png',
        active=True)


def test_interface_create(interface: IEvent):
    assert interface


def test_interface_works(interface: IEvent):
    new_event: Event = Event(**interface)
    assert new_event
