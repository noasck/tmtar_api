from flask import request, jsonify
from flask_accepts import accepts, responds
from flask_restx import Namespace, Resource
from flask.wrappers import Response
from typing import List

from .schema import LocationSchema, LocationUpdateSchema
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
        """Get all locations roots."""
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

    @api.doc(responses={200: """{"status": "Match",\n "locations": [Location Model object]}"""})
    def get(self, str_to_find: str) -> Response: # noqa
        """Get matching locations"""
        locs: List[Location] = LocationService.search_by_name(str_to_find)
        if locs:
            serialized_locations = LocationSchema().dump(locs, many=True)
            return jsonify(dict(status='Match', locations=serialized_locations))
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

    @root_required
    def delete(self, locationId: int): # noqa
        """Delete single Location"""

        deleted_id = LocationService.delete_by_id(locationId)

        return jsonify(dict(status="Success", id=deleted_id))

    @accepts(schema=LocationUpdateSchema, api=api)
    @responds(schema=LocationSchema, api=api)
    @root_required
    def put(self, locationId: int): # noqa
        """Update single Location"""

        changes: ILocation = request.parsed_obj
        loc: Location = LocationService.get_by_id(locationId)
        return LocationService.update(loc, changes)

@api.route('/children/<int:locationId>')  # noqa
@api.param('locationId', 'Location\'s db ID')
class LocationParentIdResource(Resource):
    @responds(schema=LocationSchema(many=True), api=api)
    def get(self, locationId: int): # noqa
        """ Get children of Location instance"""
        return LocationService.get_children(locationId)


@api.route('/parent/<int:childId>')  # noqa
@api.param('childId', 'Location\'s db ID')
class LocationChildrenIdResource(Resource):
    @responds(schema=LocationSchema, api=api)
    def get(self, childId: int):  # noqa
        """ Get parent of Location instance"""
        return LocationService.get_parent(LocationService.get_by_id(childId))
