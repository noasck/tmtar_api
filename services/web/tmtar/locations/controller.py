import http
from typing import List

from flask import jsonify, request
from flask_accepts import accepts, responds
from flask_cors import cross_origin
from flask_restx import Namespace, Resource, abort

from ..project.decorators.access_control import access_restriction
from ..project.types import Role
from .interface import ILocation
from .model import Location
from .schema import LocationSchema, LocationUpdateSchema
from .service import LocationService

api = Namespace(
    'locations',
    description='Ns with Location entity',
    decorators=[cross_origin()],
)


@api.route('/')
class LocationResource(Resource):
    """Locations."""

    @responds(schema=LocationSchema(many=True), api=api)
    def get(self) -> List[Location]:
        """Get all Locations instances."""
        return LocationService.get_all()

    @accepts(schema=LocationSchema, api=api)
    @responds(schema=LocationSchema, api=api)
    @access_restriction(required_role=Role.root, api=api)
    def post(self) -> Location:
        """Create Location with custom or default(0) parent."""
        return LocationService.create(request.parsed_obj)


@api.route('/search/<string:str_to_find>')
@api.param('str_to_find', 'Part of location name to search')
class LocationSearchResource(Resource):
    """Providing Location search."""

    @api.doc(responses={
        200: '{"status": "Match",\n "locations": [Location Model object]}',
        404: '{"status": "No match"}',
    })
    def get(self, str_to_find: str):
        """Get matching locations."""
        locs: List[Location] = LocationService.search_by_name(str_to_find)
        if locs:
            serialized_locations = LocationSchema().dump(locs, many=True)
            return jsonify(
                {'status': 'Match', 'locations': serialized_locations},
            )
        return jsonify({'status': 'No match'}), 404


@api.route('/<int:location_id>')
@api.param('location_id', 'Locations db ID')
class LocationIdResource(Resource):

    @responds(schema=LocationSchema, api=api)
    def get(self, location_id: int):
        """Get specific Location instance."""
        return LocationService.get_by_id(location_id)

    @api.doc(
        responses={
            200: "{'status': 'Success', 'id': deleted_id}",
        },
    )
    @access_restriction(required_role=Role.root, api=api)
    def delete(self, location_id: int):
        """Delete single Location."""
        if location_id == 1:
            abort(
                message='Cannot delete root location.',
                code=http.HTTPStatus.FORBIDDEN.value,
            )

        deleted_id = LocationService.delete_by_id(location_id)

        return jsonify({'status': 'Success', 'id': deleted_id})

    @accepts(schema=LocationUpdateSchema, api=api)
    @responds(schema=LocationSchema, api=api)
    @access_restriction(required_role=Role.root, api=api)
    def put(self, location_id: int):
        """Update single Location."""
        changes: ILocation = request.parsed_obj
        loc: Location = LocationService.get_by_id(location_id)
        return LocationService.update(loc, changes)


@api.route('/parent/<int:location_id>')
@api.param('location_id', "Location's db ID")
class LocationChildrenIdResource(Resource):

    @responds(schema=LocationSchema, api=api)
    def get(self, location_id: int):
        """Get parent of Location instance."""
        return LocationService.get_parent(
            LocationService.get_by_id(location_id),
        )
