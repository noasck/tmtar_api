from flask import request, jsonify
from flask_accepts import accepts, responds
from flask_restplus import Namespace, Resource, abort
from flask.wrappers import Response
from typing import List, Tuple
from .schema import UserSchema, UserInfoSchema
from .service import UserService
from .interface import IUser
from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt_claims
)
from .controller_identity import *
from ..project.access_control import root_required

api = Namespace('users', description='Ns responsible for User entity management and auth')

#: TODO: google auth


@api.route('/')
class UserResource(Resource):
    '''Users'''

    @responds(schema=UserSchema(many=True), api=api)
    @root_required
    def get(self) -> List[User]:
        '''Get all users'''
        return UserService.get_all()

    @accepts(schema=UserInfoSchema, api=api)
    @responds(schema=UserSchema, api=api)
    @jwt_required
    def put(self) -> Tuple[Response, int]:
        claim = get_jwt_claims()
        usr = UserService.get_by_id(claim['id'])
        changes: IUser = request.parsed_obj
        if usr:
            usr_upd = UserService.update(usr, changes)
            return usr_upd
        else:
            return abort(404, message="User not found")



@api.route('/login/<string:token>')
@api.param('token', 'Client Id or Client Token from Google or Facebook')
class UserLoginResource(Resource):
    '''Providing User auth and private data'''

    @api.doc(responses={403: 'Invalid email',
                        200: '{ststus: OK, access_token: token}'})
    def get(self, token: str):
        '''Get internal API token from Google-token'''
        identity = verify_token(token)
        if identity:
            usr = UserService.get_or_new_by_email(identity)
            access_token = create_access_token(identity=usr)
            ret = {'status': 'OK', 'access_token': access_token}

            return jsonify(ret)
        return abort(403, message="Forbidden!")

    @api.doc(responses={403: 'Invalid email',
                        200: '{ststus: OK, access_token: token}'})
    def post(self, token: str) -> Tuple[Response, int]:
        '''Get internal API token from FB-token'''
        identity = verify_token(token)
        if identity:
            usr = UserService.get_or_new_by_email(identity)
            access_token = create_access_token(identity=usr)
            ret = {'status': 'OK', 'access_token': access_token}

            return jsonify(ret), 200
        return abort(403, message="Forbidden!")


@api.route('/<int:userId>')
@api.param('userId', 'User db ID')
class LocationIdResource(Resource):

    @responds(schema=UserSchema, api=api)
    @root_required
    def get(self, userId: int ):
        ''' Get specific User instance'''

        return UserService.get_by_id(userId)

    @root_required
    def delete(self, userId: int):
        '''Delete single User'''

        deleted_id = UserService.delete_by_id(userId)

        return jsonify(dict(status="Success", id=deleted_id))

    @accepts(schema=UserSchema, api=api)
    @responds(schema=UserSchema, api=api)
    @root_required
    def put(self, userId: int):
        '''Update single User'''

        changes: IUser = request.parsed_obj
        loc: User = UserService.get_by_id(userId)
        return UserService.update(loc, changes)


