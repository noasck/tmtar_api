from datetime import datetime
from random import random
from unittest.mock import patch

from flask.testing import FlaskClient
from flask_jwt_extended import get_jti
from pytest import fixture  # noqa

from ..project.types import *
from ..tests.fixtures import app, client, token  # noqa
from . import BASE_ROUTE
from .interface import IUser
from .model import User
from .schema import UserSchema
from .service import UserService

dt = datetime.now().date()


def get_auth_header(token: str):
    return {"Authorization": f"Bearer {token}"}


def make_common_user(identity: str, id=int(1000 * random()), bdate: int = dt) -> User:  # noqa
    return User(id=id,
                identity=identity,
                sex=SexType[0],
                bdate=bdate,
                location_id=1)


def make_root_user() -> User:
    return User(id=1,
                identity=str(hash("some_str_admin")),
                sex=SexType[0],
                bdate=datetime.now().date(),
                location_id=1,
                admin_location_id=1)


def make_update(usr: User, usr_upd: IUser) -> User:
    usr.update(usr_upd)
    return usr


@patch.object(UserService, "get_or_new_by_identity",
              lambda identity: make_root_user())
def create_token(client: FlaskClient):
    with client:
        result = client.get(
            f"/api/{BASE_ROUTE}/login", headers=get_auth_header('token_sample')).get_json()
        return result['access_token']


class TestUserLoginResource:

    @patch.object(UserService, "get_or_new_by_identity",
                  lambda identity: make_common_user(identity))
    def test_token(self, client: FlaskClient):
        with client:
            result = client.get(
                f"/api/{BASE_ROUTE}/login", headers=get_auth_header('token_sample')).get_json()
            assert get_jti(result['access_token'])


class TestUserCurrentResource:

    @patch.object(UserService, "get_by_id",
                  lambda id: make_common_user('sdfsdf', 1))
    def test_get(self, client: FlaskClient, token):
        with client:
            result = client.get(
                f"/api/{BASE_ROUTE}/profile",
                headers={
                    "Authorization": f"Bearer {token}"
                },
            )
            expected = UserSchema().dump(
                make_common_user('sdfsdf', 1)
            )
            return result == expected


class TestUserResource:

    @patch.object(UserService, "get_all", lambda: [
        make_root_user(),
        make_common_user("sample-1@identity.com"),
        make_common_user("sample-2@identity.com")
    ])
    def test_get(self, client: FlaskClient, token: str):
        with client:
            result = client.get(f"/api/{BASE_ROUTE}/",
                                headers={
                                    "Authorization": f"Bearer {token}"
                                },
                                follow_redirects=True).get_json()
            expected = UserSchema(many=True).dump([
                make_root_user(),
                make_common_user("sample-1@identity.com"),
                make_common_user("sample-2@identity.com")
            ])
            for i in result:
                assert i in expected

    @patch.object(
        UserService,
        "get_by_id",
        lambda id: make_root_user()  # noqa
    )
    @patch.object(UserService, "update", lambda usr, upd: make_update(usr, upd))
    def test_put(self, client: FlaskClient, token):
        with client:
            result = client.put(f"/api/{BASE_ROUTE}/",
                                headers={
                                    "Authorization": f"Bearer {token}"
                                },
                                json={
                                    "location_id": 1,
                                    "bdate": '2018-03-09'
                                }).get_json()

            expected = UserSchema().dump(
                User(id=1,
                     identity=str(hash("some_str_admin")),
                     sex=SexType[0],
                     bdate=datetime.strptime('2018-03-09', '%Y-%m-%d').date(),
                     location_id=1,
                     admin_location_id=1))

            assert result == expected


class TestUserIdResource:

    @patch.object(
        UserService,
        "get_by_id",
        lambda user_id: make_common_user(identity='str1', id=user_id),
    )
    def test_get(self, client: FlaskClient, token: str):
        with client:
            result = client.get(f"/api/{BASE_ROUTE}/13",
                                headers={
                                    "Authorization": f"Bearer {token}"
                                },
                                follow_redirects=True).get_json()
            expected = (UserSchema().dump(make_common_user(identity='str1',
                                                           id=13),))
            assert result == expected

    @patch.object(UserService, "delete_by_id", lambda user_id: user_id)
    def test_delete(self, client: FlaskClient, token: str):
        with client:
            result = client.delete(f"/api/{BASE_ROUTE}/13",
                                   headers={
                                       "Authorization": f"Bearer {token}"
                                   },
                                   follow_redirects=True).get_json()
            expected = dict(status="Success", id=13)
            assert result == expected

    @patch.object(UserService, "get_by_id",
                  lambda user_id: make_common_user(identity='string', id=user_id))
    @patch.object(UserService, "update", make_update)
    def test_put(self, client: FlaskClient, token: str):
        with client:
            result = client.put(f"/api/{BASE_ROUTE}/13",
                                headers={
                                    "Authorization": f"Bearer {token}"
                                },
                                follow_redirects=True,
                                json={
                                    "admin_location_id": '1'
                                }).get_json()

            expected = (UserSchema().dump(
                User(id=13,
                     identity='string',
                     sex=SexType[0],
                     bdate=dt,
                     location_id=1,
                     admin_location_id=1)))
            assert result == expected
