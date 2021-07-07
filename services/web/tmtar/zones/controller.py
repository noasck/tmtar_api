from flask import jsonify, request
from flask_accepts import accepts, responds
from flask_cors import cross_origin
from flask_restx import Namespace, Resource

from ..project.decorators.access_control import access_restriction
from ..project.types import Role
from .schema import ZoneSchema, ZoneUpdateSchema
from .service import SecureZoneService

api = Namespace(
    'zones',
    description='Ns with Zone entity',
    decorators=[cross_origin()],
)

admin_location_field = 'admin_location_id'


@api.route('/')
class ZonesResource(Resource):
    """Zone instance."""

    @accepts(schema=ZoneSchema, api=api)
    @responds(schema=ZoneSchema, api=api)
    @access_restriction(
        required_role=Role.admin,
        api=api,
        inject_claims=True,
    )
    def post(self, claims):
        """Create new Zone instance."""
        return SecureZoneService.create(
            request.parsed_obj,
            user_admin_location_id=claims[admin_location_field],
        )

    @responds(schema=ZoneSchema(many=True), api=api)
    @access_restriction(
        required_role=Role.admin,
        api=api,
        inject_claims=True,
    )
    def get(self, claims):
        """Get all accessible zones."""
        return SecureZoneService.get_by_location_id(
            user_admin_location_id=claims[admin_location_field],
        )


@api.param('zone_id', 'Zone instance db ID')
@api.route('/<int:zone_id>')
class ZoneIdResource(Resource):
    """Manipulating Zone with Id."""

    @accepts(schema=ZoneUpdateSchema, api=api)
    @responds(schema=ZoneSchema, api=api)
    @access_restriction(
        required_role=Role.admin,
        api=api,
        inject_claims=True,
    )
    def put(self, zone_id, claims):
        """Update Zone by id with specific values."""
        return SecureZoneService.update_by_id(
            zone_id=zone_id,
            zone_upd=request.parsed_obj,
            user_admin_location_id=claims[admin_location_field],
        )

    @responds({'name': 'status', 'type': int}, {'name': 'id', 'type': 'int'}, api=api)
    @access_restriction(
        required_role=Role.admin,
        api=api,
        inject_claims=True,
    )
    def delete(self, zone_id: int, claims):
        """Delete single Zone by id."""
        deleted_id = SecureZoneService.delete_by_id(
            zone_id,
            user_admin_location_id=claims[admin_location_field],
        )

        return jsonify({'status': 'Success', 'id': deleted_id})
