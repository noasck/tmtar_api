from typing import List, Union
from .model import Location
from ..injectors.app import FlaskApp
from .interface import ILocation


db = FlaskApp.Instance().database


class LocationService:
    @staticmethod
    def get_all() -> List[Location]:
        return Location.query.all()

    @staticmethod
    def get_by_id(location_id: int) -> Location:
        return Location.query.get_or_404(location_id)

    @staticmethod
    def update(loc: Location, loc_upd: ILocation):
        loc.update(loc_upd)
        db.session.commit()
        return loc

    @staticmethod
    def delete_by_id(location_id: int) -> List[int]:
        loc = Location.query.filter_by(id=location_id).first_or_404()
        if not loc:
            return []
        db.session.delete(loc)
        db.session.commit()
        return [location_id]

    @staticmethod
    def get_parent(child: Location) -> Union[Location, None]:
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

        def lower(x: str):
            return x.lower()

        return [city for city in cities if lower(city.name).find(lower(str_to_search)) != -1]

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

    @staticmethod
    def check_location_permission(location_id: int, accessed_location_id: int) -> bool:
        loc = LocationService.get_by_id(location_id)
        has_access = False
        if accessed_location_id == 0:
            return True
        while loc is not None:
            if loc.id == accessed_location_id:
                has_access = True
            loc = LocationService.get_parent(loc)
        return has_access
