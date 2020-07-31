import enum


class RoleType(enum.Enum):
    COMMON = "common"
    ADMIN = "administrator"
    ROOT = 'root'


class SexType(enum.Enum):
    MALE = 'male'
    FEMALE = 'female'
    OTHER = 'undefined'
