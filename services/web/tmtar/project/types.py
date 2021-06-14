import enum

SexType = ['male', 'female', 'other']
EventType = ['news', 'sales']


class Role(enum.Enum):
    """Levels of access provided by API."""

    user = 'loggedIn'
    admin = 'admin'
    root = 'root'
