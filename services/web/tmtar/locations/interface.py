from typing_extensions import TypedDict


class ILocation(TypedDict, total=False):
    id: int
    name: str
    root: int
