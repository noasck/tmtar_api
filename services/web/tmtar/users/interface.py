from typing_extensions import TypedDict
from ..project.types import RoleType, SexType


class IUser(TypedDict, total=False):
    id: int
    email_hash: str
    age: int
    location_id: int
    sex: SexType
    role: RoleType
    admin_location_id: int
