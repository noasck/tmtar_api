from typing import List, Tuple

from flask import jsonify, request
from flask.wrappers import Response
from flask_accepts import accepts, responds
from flask_cors import cross_origin
from flask_jwt_extended import get_jwt, jwt_required  # noqa: WPS319
from flask_restx import Namespace, Resource, abort

from ..project.builders.access_control import access_restriction
from ..project.injector import Injector
from .controller_identity import create_internal_jwt, get_payload
from .schema import UserAdminLocationIdSchema, UserInfoSchema, UserSchema
from .service import IUser, User, UserService

# get previously injected auth provider
verify_token = Injector.verify_token


api = Namespace(
    'users',
    description='Ns responsible for User entity management and auth',
    decorators=[cross_origin()],
)


@api.route('/')
class UserResource(Resource):
    """Users."""

    @responds(schema=UserSchema(many=True), api=api)
    @access_restriction(root_required=True, api=api)
    def get(self) -> List[User]:
        """Get all users."""
        return UserService.get_all()

    @accepts(schema=UserInfoSchema, api=api)
    @responds(schema=UserSchema, api=api)
    @api.doc(security='loggedIn')
    @jwt_required()
    def put(self) -> Tuple[Response, int]:
        """Update info of current User."""
        claim = get_jwt()
        usr = UserService.get_by_id(claim['id'])
        changes: IUser = request.parsed_obj
        if usr:
            return UserService.update(usr, changes)
        return abort(404, message='User not found.')  # noqa: WPS432


@api.route('/login')
class UserLoginResource(Resource):
    """Provide User login. Acquire access and refresh tokens."""

    @api.doc(responses={
        403: 'Invalid identity',
        401: 'Invalid token',
        200: '{status: OK, access_token: token}',
    })
    @api.doc(security='auth0_login')
    def get(self):
        """Get internal API token from Auth0-token."""
        token = get_payload()
        identity = verify_token(token)
        if identity:
            usr = UserService.get_or_new_by_identity(identity)
            access_token = create_internal_jwt(user=usr)
            ret = {'status': 'OK', 'access_token': access_token}

            return jsonify(ret)
        return abort(403, message='Forbidden!')  # noqa: WPS432


@api.route('/<int:user_id>')
@api.param('userId', 'User db ID')
class UserIdResource(Resource):

    @responds(schema=UserSchema, api=api)
    @access_restriction(root_required=True, api=api)
    def get(self, user_id: int):
        """Get specific User instance."""
        return UserService.get_by_id(user_id)

    @access_restriction(root_required=True, api=api)
    def delete(self, user_id: int):
        """Delete single User."""
        deleted_id = UserService.delete_by_id(user_id)

        return jsonify({'status': 'Success', 'id': deleted_id})

    @accepts(schema=UserAdminLocationIdSchema, api=api)
    @responds(schema=UserSchema, api=api)
    @access_restriction(root_required=True, api=api)
    def put(self, user_id: int):
        """Update single User."""
        changes: IUser = request.parsed_obj
        loc: User = UserService.get_by_id(user_id)
        return UserService.update(loc, changes)
