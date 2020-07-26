from typing import List, Union
from .model import Location
from ..project import FlaskApp
from .interface import ILocation

db = FlaskApp.Instance().database


class LocationService:
    @staticmethod
    def get_all() -> List[Location]:
        return Location.query.all()

    @staticmethod
    def get_by_id(id: int) -> Location:
        return Location.query.get_or_404(id)

    @staticmethod
    def update(loc: Location, loc_upd: ILocation):
        loc.update(loc_upd)
        db.session.commit()
        return loc

    @staticmethod
    def delete_by_id(id: int) -> List[int]:
        loc = Location.query.filter_by(id=id).first_or_404()
        if not loc:
            return []
        db.session.delete(loc)
        db.session.commit()
        return [id]

    @staticmethod
    def get_parent(child_id: int) -> Union[Location, None]:
        child = LocationService.get_by_id(child_id)
        if child.root != 0:
            return LocationService.get_by_id(child.root)
        else:
            return None

    @staticmethod
    def get_roots() -> List[Location] or None:
        return Location.query.filter_by(root='0').all()

    @staticmethod
    def search_by_name(str_to_search: str) -> List[Location] or None:
        cities = LocationService.get_all()
        l = lambda x: x.lower()
        return [city for city in cities if l(city.name).find(l(str_to_search)) != -1]


    @staticmethod
    def get_children(parent_id: int) -> List[Location]:
        return Location.query.filter_by(root=parent_id).all()

    @staticmethod
    def create(new_loc: ILocation):
        loc = Location(
            name=new_loc['name'],
            root=new_loc['root']
        )
        db.session.add(loc)
        db.session.commit()

        return loc
