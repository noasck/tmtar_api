from typing_extensions import TypedDict


class IUser(TypedDict, total=False):
    id: int
    email_hash: str
    bdate: str
    location_id: int
    sex: str
    role: str
    admin_location_id: int
