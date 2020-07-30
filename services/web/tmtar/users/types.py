import enum


class RoleType(enum.Enum):
    COMMON = "common user"
    ADMIN = "administrator"


class SexType(enum.Enum):
    MALE = 'male'
    FEMALE = 'female'
    OTHER = 'undefined'
