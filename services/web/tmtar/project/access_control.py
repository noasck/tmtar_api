from flask_jwt_extended import jwt_required, get_jwt_claims, verify_jwt_in_request
from werkzeug.exceptions import abort
from functools import wraps
from .types import RoleType


def admin_required(endpoint):
    @wraps(endpoint)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if claims['role'] == RoleType.ADMIN:
            endpoint(*args, **kwargs)
        else:
            abort(403)


def root_required(endpoint):
    @wraps(endpoint)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if claims['role'] == RoleType.ROOT:
            endpoint(*args, **kwargs)
        else:
            abort(403)
