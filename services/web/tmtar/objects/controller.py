from flask import request, jsonify
from flask_accepts import accepts, responds
from flask_restx import Namespace, Resource
from flask.wrappers import Response
from typing import List
from flask_cors import cross_origin

from .schema import ObjectSchema
from .service import ObjectService
from .model import Object
from .interface import IObject
from ..project.builders.access_control import access_restriction

api = Namespace("objects", description="Ns with Object entity", decorators=[cross_origin()])


@api.route('/')
class ObjectResource(Resource):
    """Objects"""

    @responds(schema=ObjectSchema(many=True), api=api)
    def get(self) -> List[Object]:
        """Get all Objects."""
        return ObjectService.get_all()

    @accepts(schema=ObjectSchema, api=api)
    @responds(schema=ObjectSchema, api=api)
    @access_restriction(api=api)
    def post(self) -> Object:
        """Create new Object"""
        return ObjectService.create(request.parsed_obj)

@api.route('/<int:objectId>') # noqa
@api.param('objectId', 'object db ID')
class ObjectIdResource(Resource):
    """Provides Object manipulations by id"""

    @responds(schema=ObjectSchema, api=api)
    def get(self, objectId: int) -> Object:
        """Get specific Object instance by id"""
        return ObjectService.get_by_id(objectId)

    @accepts(schema=ObjectSchema, api=api)
    @responds(schema=ObjectSchema, api=api)
    @access_restriction(api=api)
    def put(self, objectId: int) -> Object:
        """Updates Object by id"""

        object_to_update = ObjectService.get_by_id(objectId)
        changes: IObject = request.parsed_obj
        return ObjectService.update(object_to_update, changes)

    @api.doc(responses={200: "{\"status\": \"Success\", \"id\" = 1}"})
    @access_restriction(root_required=True, api=api)
    def delete(self, objectId: int):
        """Delete single Object"""

        deleted_id = ObjectService.delete_by_id(objectId)
        return jsonify(status="Success", id=deleted_id)

@api.route('/subzone/<int:subzoneId>') # noqa
@api.param('subzoneId', 'subzone db ID')
class ObjectSubzoneIdResource(Resource):
    """Provides objects manipulation by subzone id"""

    @responds(schema=ObjectSchema(many=True), api=api)
    def get(self, subzoneId: int) -> List[Object]:
        """Get all Objects from specific subzone."""
        return ObjectService.get_by_subzone_id(subzoneId)

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
            return jsonify(dict(status='Match', objects=serialized_objects))
        else:
            return jsonify(dict(status="No match"))
