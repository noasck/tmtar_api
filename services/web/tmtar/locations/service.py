from typing import List, Union
from .model import Location
from ..project.injector import Injector
from .interface import ILocation
from flask_restx import abort


db = Injector().db


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
        for child in LocationService.get_children(loc.id):
            LocationService.delete_by_id(child.id)
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
    def get_root() -> Location or None:
        return Location.query.filter_by(name='root').first_or_404()

    @staticmethod
    def search_by_name(str_to_search: str) -> List[Location] or None:
        return Location.query.filter(Location.name.ilike(f"%{str_to_search}%")).all()

    @staticmethod
    def get_children(parent_id: int) -> List[Location]:
        return Location.query.filter_by(root=parent_id).all()

    @staticmethod
    def create(new_loc: ILocation):
        loc = Location(**new_loc)
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
