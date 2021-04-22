from typing import List, Tuple

from flask import jsonify, request
from flask.wrappers import Response
from flask_accepts import accepts, responds
from flask_cors import cross_origin
from flask_jwt_extended import create_access_token  # noqa: WPS318
from flask_jwt_extended import get_jwt_claims, jwt_required  # noqa: WPS319
from flask_restx import Namespace, Resource, abort

from ..project.builders.access_control import access_restriction
from .controller_identity import verify_token
from .schema import UserAdminLocationIdSchema, UserInfoSchema, UserSchema
from .service import IUser, User, UserService

api = Namespace(
    'users',
    description='Ns responsible for User entity management and auth',
    decorators=[cross_origin()],
)

#: TODO: google auth


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
    @jwt_required
    def put(self) -> Tuple[Response, int]:
        """Update info of current User."""
        claim = get_jwt_claims()
        usr = UserService.get_by_id(claim['id'])
        changes: IUser = request.parsed_obj
        if usr:
            return UserService.update(usr, changes)
        return abort(404, message='User not found.')  # noqa: WPS432


@api.route('/login/<string:token>')
@api.param('token', 'Client Id or Client Token from Google or Facebook')
class UserLoginResource(Resource):
    """Providing User auth and private data."""

    # TODO: refactor - make 2 GET routes for fb and google with OWN SCHEMA.

    @api.doc(responses={
        403: 'Invalid email',
        200: '{status: OK, access_token: token}',
    })
    def get(self, token: str):
        """Get internal API token from Google-token."""
        identity = verify_token(token)
        if identity:
            usr = UserService.get_or_new_by_email(identity)
            access_token = create_access_token(identity=usr)
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
