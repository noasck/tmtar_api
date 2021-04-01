class Injector:
    """Storage to inject dependencies."""

    __storage = dict()

    def inject(self, instance, to="name"): # noqa
        """
        Method that assigns internal static field to instance link.
        @param instance: instance to save in database.
        @param to: name of instance.
        """
        Injector().__storage[to] = instance

    def __getattr__(self, instance_name: str):
        """
        Returns saved in static field instance.
        @param instance_name: name of instance.
        @return: required function or instance.
        """
        try:
            return Injector().__storage[instance_name]
        except KeyError:
            raise AttributeError(instance_name+" doesn't exist in this scope.")
