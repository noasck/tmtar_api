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

admin_location_field = 'admin_location_id'


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
        """Create new event instance."""
        return SecureEventService.create(
            request.parsed_obj,
            user_admin_location_id=claims[admin_location_field],
        )


@api.route('/all/<int:page>')
class PaginatedEventsResource(Resource):
    """Paginated Events resource."""

    @responds(schema=EventSchema(many=True), api=api)
    @access_restriction(
        required_role=Role.admin,
        api=api,
        inject_claims=True,
    )
    def get(self, page: int, claims):
        """Get all events for editing."""
        return SecureEventService.get_all(
            user_admin_location_id=claims[admin_location_field],
            page=page,
        )


@api.route('/all/search/<string:str_to_find>')
@api.param('str_to_find', 'Part of Event title to search')
class EventsSearchResource(Resource):
    """Providing Events search."""

    @api.doc(responses={
        200: '{"status": "Match",\n "events": [Event Model object]}',
        404: '{"status": "No match"}',
    })
    @access_restriction(
        required_role=Role.admin,
        api=api,
        inject_claims=True,
    )
    def get(self, str_to_find: str, claims):
        """Get matching events by part of title."""
        events = SecureEventService.search_by_title(
            str_to_find,
            user_admin_location_id=claims[admin_location_field],
        )
        if events:
            serialized_events = EventSchema().dump(events, many=True)
            return jsonify(
                {'status': 'Match', 'events': serialized_events},
            )
        return jsonify({'status': 'No match'}), 404


@api.route('/all/count')
class EventsCountResource(Resource):
    """Events count resource."""

    @api.doc(
        responses={
            200: "{'count': int}",
        },
    )
    @access_restriction(
        required_role=Role.admin,
        api=api,
        inject_claims=True,
    )
    def get(self, claims):
        """Get count of all accessible events."""
        events_count = SecureEventService.count_all_events(
            user_admin_location_id=claims[admin_location_field],
        )
        return jsonify(
            {'count': events_count},
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
            user_admin_location_id=claims[admin_location_field],
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
            user_admin_location_id=claims[admin_location_field],
        )

        return jsonify({'status': 'Success', 'id': deleted_id})
