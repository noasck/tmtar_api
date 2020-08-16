from typing_extensions import TypedDict


class IEvent(TypedDict):
    id: int
    event_type: str
    location_id: int
    update_date: int
    sex: str
    min_age: int
    max_age: int
    title: str
    short_description: str
    description: str
    image_file_name: str
    active: bool
