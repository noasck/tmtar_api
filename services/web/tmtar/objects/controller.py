from flask import request, jsonify
from flask_accepts import accepts, responds
from flask_restx import Namespace, Resource
from flask.wrappers import Response
from typing import List

from .schema import ObjectSchema
from .service import ObjectService
from .model import Object
from .interface import IObject
from ..project.access_control import root_required, admin_required

api = Namespace("objects", description="Ns with Object entity")


@api.route('/')
class ObjectResource(Resource):
    """Objects"""

    @responds(schema=ObjectSchema(many=True), api=api)
    def get(self) -> List[Object]:
        """Get all Objects."""
        return ObjectService.get_all()

    @accepts(schema=ObjectSchema, api=api)
    @responds(schema=ObjectSchema, api=api)
    @admin_required
    def post(self) -> Object:
        """Create new Object"""
        return ObjectService.create(request.parsed_obj)

@api.route('/<int:objectId>') # noqa
@api.param('objectId', 'object db ID')
class ObjectIdResource(Resource):
    """Provides Object manipulations by id"""

    @responds(schema=ObjectSchema, api=api)
    def get(self, object_id: int) -> Object:
        """Get specific Object instance by id"""
        return ObjectService.get_by_id(object_id)

    @accepts(schema=ObjectSchema, api=api)
    @responds(schema=ObjectSchema, api=api)
    @admin_required
    def put(self, object_id: int) -> Object:
        """Updates Object by id"""

        object_to_update = ObjectService.get_by_id(object_id)
        changes: IObject = request.parsed_obj
        return ObjectService.update(object_to_update, changes)

    @api.doc(responses={200: "{\"status\": \"Success\", \"id\" = 1}"})
    @root_required
    def delete(self, object_id: int):
        """Delete single Object"""

        deleted_id = ObjectService.delete_by_id(object_id)
        return jsonify(status="Success", id=deleted_id)

@api.route('/subzone/<int:subzoneId>') # noqa
@api.param('subzoneId', 'subzone db ID')
class ObjectSubzoneIdResource(Resource):
    """Provides objects manipulation by subzone id"""

    @responds(schema=ObjectSchema(many=True), api=api)
    def get(self, subzone_id: int) -> List[Object]:
        """Get all Objects from specific subzone."""
        return ObjectService.get_by_subzone_id(subzone_id)

@api.route('/search/<string:str_to_find>') # noqa
@api.param('str_to_find', 'Part of Object name to search')
class ObjectSearchResource(Resource):
    """Providing Object search"""

    @api.doc(responses={200: """{"status": "Match",\n "objects": [Object Model list]}"""})
    def get(self, str_to_find: str) -> Response: # noqa
        """Get matching objects"""
        objects: List[Object] = ObjectService.search_by_name(str_to_find)
        if objects:
            serialized_objects = ObjectSchema().dump(objects, many=True)
            return jsonify(dict(status='Match', locations=serialized_objects))
        else:
            return jsonify(dict(status="No match"))
