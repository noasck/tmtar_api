## Versions
### s.031 (Current)
#### Changes:
1. Added ```/all/count``` and ```/all/search/<str_to_search>``` **Event** resource routes.
2. Added related tests.

--------------------------------------------------------
### s.03
#### Changes:
1. Added Events service.
2. Added token expiration and refreshing.

--------------------------------------------------------

### s.021
#### Changes:
1. Added Authorization for ```/users/login``` route documentation
2. Migrated to Python 3.9 and newest versions of libraries (except ```flake8```, pinned).
3. Added monkeypatch for *flask.scafold*. Waiting for upd's in the *flask-restx* package.

--------------------------------------------------------
### s.02
#### Changes:

1. ```api/users/login``` route: need to pass ```Authorization: Bearer ``` header with **Auth0** ```access_token```
2. Important. No **need to manage database manually**.
    1. Excluded *Migrations* from ```entrypoint```. That means, database is clear at every run.
    2. ```drop_all/set_up``` in entrypoint. While not release version, database fully reinits at every build.
    2. Fulfilled migration support for multiple databases has been added to *TODO-list*.
    3. Deleted deprecated **Flask-Script** and **Flask-Migrate** in order to use pure **Alembic** for migrations.
4. Deleted ```access.log```. All outputs are on the stdout. *TODO: look for a solution.*
5. Changed **CLI** commands.
#### Next up:

- Token expiration.
- Token exceptions handling.
- Events instance and routes.
------------------------------------------------------
### s.01
All previous versions of API tagged as s.01

