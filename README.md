## Basic information

[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)

#### Pre-commit checks:
- Styleguide: **OK** (0 warnings)
- Tests: **OK** (108/108 passed)

#### Contacts 
```@you2ku``` at **Telegram**.

#### Changelog
For more information about versions please check [Changelog](https://gitlab.com/baltazar1697/tmtar_api/-/blob/df4ac122e9b35c7aede9b49b489aeaaf03959b36/CHANGELOG.md)

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

### Accessing API
In **development** you can use *Swagger OpenAPI* documentation to check routes you need and view namespaces, schemas, parameters, route's information.
- **Development:** ```http://localhost:5000```.

API itself:
- **Production:** ```http://localhost:1337/api/```.
- **Development:** ```http://localhost:5000/api/```.

## Database administration
We use PostgreSQL as our major database. Project requires some tables and root records to be created for correct runnning.
There several ways to **set up database** with all tables needed.

### Production - Alembic migrations

You can use ```Flask-Migrate``` extension to set up tables **in production**:

*--TBD--*

### Manual (forced) migrations
You can recreate all tables manually by running 2 sequential commands inside the container. 
But you should be prepared for troubles. This method is highly unstable and could call some exceptions.

*--TBD--*


## Authorization
Obtaining access token is one of basic tasks while working with API.
#### Production
1. Obtain **Auth0** ```access_token```.
To do that, you need to be our team member in **Auth0** service.
   
2. Get our own API token. At this point, your request should be like (**curl** analogue): 
``` bash
curl --request GET \
--url http://localhost:1337/api/users/login \
--header 'authorization: Bearer paste_your_AUTH0_access_token'
```
You'll get an access token and refresh token as following:
``` json
{
  "access_token": "...",
  "refresh_token": "...",
  "status": "OK"
}
```


#### Testing
1. Get our own API token. At this point, your request should be like (**curl** analogue): 
``` bash
curl --request GET \
--url http://localhost:1337/api/users/login \
--header 'authorization: Bearer just_admins_identity'
```
Where ```admins_identity``` means your *root* identity - ```sub``` in testing environment.

#### Token expiration
In case token is invalid or expired, you receive the *401 UNAUTHORIZED* with following body:
```json
{
  "msg": "Token has expired"
}
```
To refresh token you need to make a request like:
``` bash
curl -X 'GET' \
  'http://0.0.0.0:5000/api/users/login' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer refresh_token'
```
As a result you acquire new access token like:
```json
{
  "access_token": "...",
  "status": "OK"
}
```

**Default timeouts** for *access* and *refresh* tokens expiration:
- **Production**: *15 minutes* and *7 days* accordingly.
- **Development**: *Never* and *Never* accordingly