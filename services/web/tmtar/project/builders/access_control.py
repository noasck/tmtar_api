from flask_jwt_extended import get_jwt_claims, verify_jwt_in_request, jwt_required
from flask_jwt_extended.exceptions import JWTExtendedException
from flask_restx import abort, Namespace
from functools import wraps
from typing import Callable


def access_restriction(root_required: bool = False, api: Namespace = None) -> Callable:
    """
    Params wrapper around access control decorator.
    @param root_required: if set, checks admin_location_id to be 0.
    @param api: api Namespace to create auth documentation.
    @return: secured endpoint wrapper.
    """
    def admin_required(endpoint):
        """
        Protects endpoint with jwt claims. Extracts user role.
        @param endpoint: route endpoint.
        """
        @api.doc(security='root' if root_required else 'admin')
        @jwt_required
        @wraps(endpoint)
        def wrapper(*args, **kwargs):
            try:
                verify_jwt_in_request()
                claims = get_jwt_claims()
                admin_location_id = int(claims['admin_location_id'])
            except (ValueError, TypeError, JWTExtendedException):
                # TODO: make more detailed JWTExtendedException response
                return abort(403, "Restricted. Access denied.")
            if root_required and admin_location_id != 1:
                return abort(403, "Restricted. Access denied.")
            return endpoint(*args, **kwargs)
        return wrapper

    return admin_required


authorizations = {
    'admin': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    },
    'root': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    },
    'loggedIn': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}
