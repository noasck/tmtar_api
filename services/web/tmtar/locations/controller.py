from flask import request, jsonify
from flask_accepts import accepts, responds
from flask_restx import Namespace, Resource
from flask.wrappers import Response
from typing import List

from .schema import LocationSchema
from .service import LocationService
from .model import Location
from .interface import ILocation
from ..project.access_control import root_required

api = Namespace('locations', description='Ns with Location entity')


@api.route('/')
class LocationResource(Resource):
    """Locations"""

    @responds(schema=LocationSchema(many=True), api=api)
    def get(self) -> List[Location]:
        """Get all locations"""
        return LocationService.get_roots()

    @accepts(schema=LocationSchema, api=api)
    @responds(schema=LocationSchema, api=api)
    @root_required
    def post(self) -> Location:
        """ Create Location with custom or default(0) parent"""

        return LocationService.create(request.parsed_obj)

@api.route('/search/<string:str_to_find>') # noqa
@api.param('str_to_find', 'Part of location name to search')
class LocationSearchResource(Resource):
    """Providing Location search"""

    def get(self, str_to_find: str) -> Response: # noqa
        """ Get tree of addresses by part of name"""
        locs = []
        for loc in LocationService.search_by_name(str_to_find):
            res = loc.name
            nxt = LocationService.get_parent(loc)
            while nxt is not None:
                res += ', ' + nxt.name
                nxt = LocationService.get_parent(nxt)
            locs.append(res)
        if locs:
            return jsonify(dict(status='Match', locations=locs))
        else:
            return jsonify(dict(status="No match"))


@api.route('/<int:locationId>') # noqa
@api.param('locationId', 'Locations db ID')
class LocationIdResource(Resource):
    @responds(schema=LocationSchema, api=api)
    @root_required
    def get(self, locationId: int): # noqa
        """ Get specific Location instance"""

        return LocationService.get_by_id(locationId)

    @responds(schema=LocationSchema(many=True), api=api)
    def post(self, locationId: int): # noqa
        """ Get children of Location instance"""
        return LocationService.get_children(locationId)

    @root_required
    def delete(self, locationId: int): # noqa
        """Delete single Location"""

        deleted_id = LocationService.delete_by_id(locationId)

        return jsonify(dict(status="Success", id=deleted_id))

    @accepts(schema=LocationSchema, api=api)
    @responds(schema=LocationSchema, api=api)
    @root_required
    def put(self, locationId: int): # noqa
        """Update single Location"""

        changes: ILocation = request.parsed_obj
        loc: Location = LocationService.get_by_id(locationId)
        return LocationService.update(loc, changes)
