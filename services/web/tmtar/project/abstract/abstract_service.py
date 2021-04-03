from abc import ABC, abstractmethod
from typing import Generic, List, Type, TypeVar

from ..injector import Injector

Model = TypeVar('Model')
Interface = TypeVar('Interface')


class AbstractService(ABC, Generic[Model, Interface]):
    """Class implements operations over an instance."""

    _db = Injector.db

    @classmethod
    @abstractmethod
    def model(cls) -> Type[Model]:
        pass

    @classmethod
    def get_all(cls) -> List[Model]:
        return cls.model().query.all()

    @classmethod
    def get_by_id(cls, instance_id: int) -> Model:
        return cls.model().query.get_or_404(instance_id)

    @classmethod
    def update(cls, instance: Model, instance_upd: Interface) -> Model:
        instance.update(instance_upd)
        cls._db.session.commit()
        return instance

    @classmethod
    def delete_by_id(cls, instance_id: int) -> int:
        loc = cls.model().query.filter_by(id=instance_id).first_or_404()
        cls._db.session.delete(loc)
        cls._db.session.commit()
        return instance_id

    @classmethod
    def create(cls, new_instance: Interface):
        loc = cls.model()(**new_instance)
        cls._db.session.add(loc)
        cls._db.session.commit()

        return loc
