from flask_jwt_extended import get_jwt_claims, verify_jwt_in_request
from flask_restx import abort
from functools import wraps
from typing import Callable


def access_restriction(root_required: bool = False) -> Callable:
    """
    Params wrapper around access control decorator.
    @param root_required: if set, checks admin_location_id to be 0
    @return: secured endpoint wrapper.
    """
    def admin_required(endpoint):
        """
        Protects endpoint with jwt claims. Extracts user role.
        @param endpoint: route endpoint.
        """
        @wraps(endpoint)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt_claims()
            try:
                admin_location_id = int(claims['admin_location_id'])
            except ValueError:
                return abort(403, "Restricted. Access denied.")
            except TypeError:
                return abort(403, "Restricted. Access denied.")
            if root_required and admin_location_id != 0:
                return abort(403, "Restricted. Access denied.")
            return endpoint(*args, **kwargs)
        return wrapper

    return admin_required
