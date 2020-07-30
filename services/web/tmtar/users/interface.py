from typing_extensions import TypedDict
from .types import RoleType, SexType


class IUser(TypedDict, total=False):
    id: int
    email_hash: str
    age: int
    location_id: int
    sex: str
    role: str
    admin_location_id: int
