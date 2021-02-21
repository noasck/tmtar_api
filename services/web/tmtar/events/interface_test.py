from ..tests.fixtures import * # noqa
import time
from pytest import fixture

from .interface import IEvent
from ..project.types import SexType, EventType
from .model import Event

time_now = int(time.time())


@fixture
def interface() -> IEvent:
    return IEvent(id=1, event_type=EventType[0], location_id=1, update_date=time_now, sex=SexType[0], min_age=12,
                  max_age=100, title="Sample", short_description="""The plugin adds a random text generator, capable 
                 of creating witty texts in different genres. Created text can be inserted newly at the caret, 
                 or replace a selection.""", description=""" The plugin adds a random text generator, capable of 
                 creating witty texts in different genres. Created text can be inserted newly at the caret, 
                 or replace a selection. The plugin adds a random text generator, capable of creating witty 
                 texts in different genres. Created text can be inserted newly at the caret, or replace a selection.""",
                  image_file_name='sample.png', active=True)


def test_interface_create(interface: IEvent):
    assert interface


def test_interface_works(interface: IEvent):
    new_event: Event = Event(**interface)
    assert new_event
