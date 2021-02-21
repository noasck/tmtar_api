from ..tests.fixtures import * # noqa
import time
from pytest import fixture

from .model import Event
from ..project.types import *

time_now = int(time.time())


@fixture
def event():
    return Event(id=1, event_type=EventType[0], location_id=1, update_date=time_now, sex=SexType[0], min_age=12,
                 max_age=100, title="Sample", short_description="""The plugin adds a random text generator, capable 
                 of creating witty texts in different genres. Created text can be inserted newly at the caret, 
                 or replace a selection.""", description=""" The plugin adds a random text generator, capable of 
                 creating witty texts in different genres. Created text can be inserted newly at the caret, 
                 or replace a selection. The plugin adds a random text generator, capable of creating witty 
                 texts in different genres. Created text can be inserted newly at the caret, or replace a selection.""",
                 image_file_name='sample.png', active=True)


def test_model_create(event: Event):
    assert event
