from unittest.mock import patch
from flask.testing import FlaskClient
from ..tests.fixtures import client, app, token # noqa
from .service import UserService
from pytest import fixture # noqa
from .model import User
from .schema import UserSchema
from .interface import IUser
from . import BASE_ROUTE
from ..project.types import *
from flask_jwt_extended import get_jti
from random import random
from datetime import datetime


def make_common_user(email: str, id=int(1000*random())) -> User: # noqa
    return User(id=id, email_hash=str(hash(email)), sex=SexType[0],
                bdate=datetime.now().date(), location_id=1, role=RoleType[0])


def make_root_user() -> User:
    return User(id=1, email_hash=str(hash("some_str_admin")), sex=SexType[0],
                bdate=datetime.now().date(), location_id=1, role=RoleType[2])


def make_update(usr: User, usr_upd: IUser) -> User:
    usr.update(usr_upd)
    return usr


@patch.object(
    UserService,
    "get_or_new_by_email",
    lambda email: make_root_user()
)
def create_token(client: FlaskClient):
    with client:
        result = client.get(f"/api/{BASE_ROUTE}/login/some_str_admin@mail.com").get_json()
        return result['access_token']


class TestUserLoginResource:
    @patch.object(
        UserService,
        "get_or_new_by_email",
        lambda email: make_common_user(email)
    )
    def test_token(self, client: FlaskClient):
        with client:
            result = client.get(f"/api/{BASE_ROUTE}/login/new-email@mail.com").get_json()
            assert get_jti(result['access_token'])


class TestUserResource:
    @patch.object(
        UserService,
        "get_all",
        lambda: [make_root_user(), make_common_user("sample-1@email.com"), make_common_user("sample-2@email.com")]
    )
    def test_get(self, client: FlaskClient, token: str):
        with client:
            result = client.get(f"/api/{BASE_ROUTE}/", headers={"Authorization": f"Bearer {token}"},
                                follow_redirects=True).get_json()
            expected = UserSchema(many=True).dump(
                [
                    make_root_user(), make_common_user("sample-1@email.com"), make_common_user("sample-2@email.com")
                ]
            )
            for i in result:
                assert i in expected

    @patch.object(
        UserService,
        "get_by_id",
        lambda id: make_root_user() # noqa
    )
    @patch.object(
        UserService,
        "update",
        lambda usr, upd: make_update(usr, upd)
    )
    def test_put(self, client: FlaskClient, token):
        with client:
            result = client.put(
                f"/api/{BASE_ROUTE}/",
                headers={"Authorization": f"Bearer {token}"},
                json={
                    "location_id": 2,
                    "bdate": '2018-03-09'
                }
            ).get_json()

            expected = UserSchema().dump(
                User(id=1, email_hash=str(hash("some_str_admin")), sex=SexType[0],
                     bdate=datetime.strptime('2018-03-09', '%Y-%m-%d').date(), location_id=2, role=RoleType[2])
            )

            assert result == expected


class TestUserIdResource:
    @patch.object(UserService, "get_by_id",
                  lambda user_id:
                  make_common_user(email='str1', id=user_id),
                  )
    def test_get(self, client: FlaskClient, token: str):
        with client:
            result = client.get(f"/api/{BASE_ROUTE}/13", headers={"Authorization": f"Bearer {token}"},
                                follow_redirects=True).get_json()
            expected = (
                UserSchema()
                .dump(
                    make_common_user(email='str1', id=13),
                )
            )
            assert result == expected

    @patch.object(UserService, "delete_by_id", lambda user_id: user_id)
    def test_delete(self, client: FlaskClient, token: str):
        with client:
            result = client.delete(f"/api/{BASE_ROUTE}/13", headers={"Authorization": f"Bearer {token}"},
                                   follow_redirects=True).get_json()
            expected = dict(status="Success", id=13)
            assert result == expected

    @patch.object(UserService, "get_by_id", lambda user_id: make_common_user(email='string', id=user_id))
    @patch.object(UserService, "update", make_update)
    def test_put(self, client: FlaskClient, token: str):
        with client:
            result = client.put(
                f"/api/{BASE_ROUTE}/13",
                headers={"Authorization": f"Bearer {token}"},
                follow_redirects=True,
                json={
                    "location_id": 2,
                    "bdate": '2018-03-09'
                }
            ).get_json()

            expected = (
                UserSchema()
                .dump(
                    User(id=13, email_hash=str(hash("string")), sex=SexType[0],
                         bdate=datetime.strptime('2018-03-09', '%Y-%m-%d').date(), location_id=2,
                         role=RoleType[0])
                )
            )
            assert result == expected
