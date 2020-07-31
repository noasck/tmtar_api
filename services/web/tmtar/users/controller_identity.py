from ..injectors.app import FlaskApp
from .model import User
from .schema import UserSchema

jwt = FlaskApp.Instance().jwt


@jwt.user_claims_loader
def user_based_token(user: User):
    '''
    Function that serialize single User entity data to JWT
    :param user: User instance
    :return: serialized User Instance
    '''
    return UserSchema().dump(user)


#: TEST: Delete
def verify_token(token: str) -> str:
    '''
    Mocking google and fb auth
    :param token: email
    :return: email
    '''
    return token.strip()


@jwt.user_identity_loader
def user_identity_lookup(user: User) -> str:
    return user.email_hash

# get_jwt_claims() -- function to unpack tokenized object


