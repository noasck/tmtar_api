from functools import wraps


class LocationChecker:
    """Singleton to inject location dependency"""

    __checker_dependency = None

    @staticmethod
    def inject_dependency(func):
        """
        Method that assigns internal static field to function
        :param func: Childhood access check function
        :return: void
        """
        LocationChecker.__checker_dependency = func

    @staticmethod
    def check(location_id: int, user_location_id: int) -> bool:
        """
        Check for childhood to access admin module
        :param location_id: Location db ID
        :param user_location_id: User admin_location_id from jwt
        :return: isChild or this
        """
        return LocationChecker.__checker_dependency(location_id, user_location_id)

    def __init__(self):
        """Singleton doesnt provide constructor"""
        raise NotImplementedError()


class Fixtures:
    """Singleton to inject token fixture dependency"""

    __token = dict()

    @staticmethod
    def inject_dependency(func):
        """Method that assigns internal static field to function"""
        Fixtures.__token[func.__name__] = func

    @staticmethod
    def get(func_name: str):
        try:
            return Fixtures.__token[func_name]
        except KeyError:
            raise RuntimeError(func_name+" doesn't exist in this scope.")

    def __init__(self):
        """Singleton doesnt provide constructor"""
        raise NotImplementedError()
