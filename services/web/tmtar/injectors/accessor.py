class LocationChecker:
    '''Singleton to inject location dependency'''

    __checker_dependency = None

    @staticmethod
    def inject_dependency(func):
        '''
        Method that assigns internal static field to function
        :param func: Childhood access check function
        :return: void
        '''
        LocationChecker.__checker_depency = func

    @staticmethod
    def check(location_id: int, user_identity) -> bool:
        '''
        Check for childhood to access admin module
        :param location_id: Location db ID
        :param user_identity: Serialized User instance
        :return: isChild or this
        '''
        return LocationChecker.__checker_dependency(location_id, user_identity['admin_location_id'])
