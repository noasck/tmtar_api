from typing_extensions import TypedDict


class IUser(TypedDict, total=False):
    id: int
    identity: str
    bdate: str
    location_id: int
    sex: str
    admin_location_id: int
