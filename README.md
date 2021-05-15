## Versions

### s.02 (Current) 

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

### s.01
All previous versions of API tagged as s.01

-----------------------------------

## Deployment

#### Useful aliases
``` bash
alias dc_build_dev='docker-compose -f docker-compose.yml up --build'
alias dc_build_test='docker-compose -f docker-compose.test.yml up --build --abort-on-container-exit'
alias dc_build_prod='docker-compose -f docker-compose.prod.yml up --build'


alias dc_down_dev='docker-compose -f docker-compose.yml down --volumes --remove-orphans'
alias dc_down_test='docker-compose -f docker-compose.test.yml down --volumes --remove-orphans'
alias dc_down_prod='docker-compose -f docker-compose.prod.yml down --volumes --remove-orphans'
```
**Optionally:** you could add ```-d``` key after alias-called script to *run docker services in the background*. 
(E.g. ```dc_build_prod -d```)
### Testing
- Up: ```dc_build_test```
- Down: ```dc_down_test```
### Development
- Up: ```dc_build_dev```
- Down: ```dc_down_dev```
### Production
- Up: ```dc_build_peod```
- Down: ```dc_down_prod```

## Database administration
We use PostgreSQL as our major database. Project requires some tables and root records to be created for correct runnning.
There several ways to **set up database** with all tables needed.

### Alembic migrations
You can use ```Flask-Migrate``` extension to set up tables:
1. At the first run, perhaps you will need to initialize *Alembic* structure: (**only for backend devs**)

``` bash
  docker-compose run web python manage.py db init
```
2. (*) You need to create and manually review migrations:
```bash
# Create migration:
docker-compose run web python manage.py db upgrade
```
3. For future runs, execute 2 commands:

``` bash
# Migrating scheme:
docker-compose run web python manage.py db upgrade
# Seed database:
docker-compose run web python manage.py seed_db
```
... and restart full application.

### Manual (forced) migrations
You can recreate all tables manually by running 2 sequential commands inside the container. 
But you should be prepared for troubles. This method is highly unstable and could call some exceptions.

``` bash
# drop all tables
docker-compose run web python manage.py tear_down
# create all tables
docker-compose run web python manage.py set_up
```


### Authorization
Obtaining access token is one of basic tasks.
#### Production
1. Obtain **Auth0** ```access_token```.
To do that, you need to be our team member in **Auth0** service.
   
2. Get our own API token. At this point, your request should be like (**curl** analogue): 
``` bash
curl --request GET \
--url http://localhost:1337/api/users/login \
--header 'authorization: Bearer paste_your_AUTH0_access_token'
```

#### Testing
1. Get our own API token. At this point, your request should be like (**curl** analogue): 
``` bash
curl --request GET \
--url http://localhost:1337/api/users/login \
--header 'authorization: Bearer just_admins_identity'
```
Where ```admins_identity``` means your *root* identity - ```sub``` in testing environment.

[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)

#### Pre-commit checks:
- Styleguide: **OK** (0 warnings)
- Tests: **OK** (73/73 passed)

#### Contacts 
```@you2ku``` at **Telegram**.
