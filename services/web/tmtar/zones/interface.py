from geoalchemy2 import Geography
from typing_extensions import TypedDict


class IZone(TypedDict, total=False):
    id: int
    title: str
    location_id: int
    center: Geography
    radius: float
    active: bool
    secret: bool
