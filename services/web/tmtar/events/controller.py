from flask import jsonify, request
from flask_accepts import accepts, responds
from flask_cors import cross_origin
from flask_restx import Namespace, Resource

from ..project.builders.access_control import access_restriction
from ..project.types import EventType, Role
from .interface import IEvent
from .schema import EventSchema, UpdateEventSchema
from .service import SecureEventService

api = Namespace(
    'events',
    description='Ns with News and Sales entity',
    decorators=[cross_origin()],
)


@api.route('/')
class EventsResource(Resource):
    """Events instance."""

    @accepts(schema=EventSchema, api=api)
    @responds(schema=EventSchema, api=api)
    @access_restriction(
        required_role=Role.admin,
        api=api,
        inject_claims=True,
    )
    def post(self, claims):
        """Get all events for editing."""
        return SecureEventService.create(
            request.parsed_obj,
            user_admin_location_id=claims['admin_location_id'],
        )


@api.route('/all/<int:page>')
class PaginatedEventsResource(Resource):
    """Events resource."""

    @responds(schema=EventSchema(many=True), api=api)
    @access_restriction(
        required_role=Role.admin,
        api=api,
        inject_claims=True,
    )
    def get(self, page: int, claims):
        """Get all events for editing."""
        return SecureEventService.get_all(
            user_admin_location_id=claims['admin_location_id'],
            page=page,
        )


@api.route('/news/<int:page>')
class PaginatedNewsResource(Resource):
    """News event type."""

    @responds(schema=EventSchema(many=True), api=api)
    @access_restriction(
        required_role=Role.user,
        api=api,
        inject_claims=True,
    )
    def get(self, page: int, claims):
        """Get latest news for current user."""
        return SecureEventService.get_by_user_location(
            event_type=EventType[0],
            user_location_id=claims['location_id'],
            page=page,
        )


@api.route('/sales/<int:page>')
class PaginatedSalesResource(Resource):
    """Sales event type."""

    @responds(schema=EventSchema(many=True), api=api)
    @access_restriction(
        required_role=Role.user,
        api=api,
        inject_claims=True,
    )
    def get(self, page: int, claims):
        """Get latest sales for current user."""
        return SecureEventService.get_by_user_location(
            event_type=EventType[1],
            user_location_id=claims['location_id'],
            page=page,
        )


@api.route('/<int:event_id>')
class EventsIdResource(Resource):
    """Events instance id resource."""

    @accepts(schema=UpdateEventSchema, api=api)
    @responds(schema=EventSchema, api=api)
    @access_restriction(
        required_role=Role.admin,
        api=api,
        inject_claims=True,
    )
    def put(self, event_id: int, claims):
        """Update single Event."""
        changes: IEvent = request.parsed_obj
        return SecureEventService.update_by_id(
            event_id,
            changes,
            user_admin_location_id=claims['admin_location_id'],
        )

    @api.doc(
        responses={
            200: "{'status': 'Success', 'id': deleted_id}",
        },
    )
    @access_restriction(
        required_role=Role.admin,
        api=api,
        inject_claims=True,
    )
    def delete(self, event_id: int, claims):
        """Delete single Event by id."""
        deleted_id = SecureEventService.delete_by_id(
            event_id,
            user_admin_location_id=claims['admin_location_id'],
        )

        return jsonify({'status': 'Success', 'id': deleted_id})
