## Deployment

#### Useful aliases
``` bash
alias dc_build_dev='docker-compose -f docker-compose.yml up --build'
alias dc_build_test='docker-compose -f docker-compose.test.yml up --build'
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
1. At the first run, perhaps you will need to initialize *Alembic* structure:

``` bash
  docker-compose run web python manage.py db init
```

2. For future runs, execute 3 commands:

``` bash
# Migrating scheme:
docker-compose run web python manage.py db migrate
# Upgrading database:
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

[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)

#### Pre-commit checks:
- Styleguide: **OK** (0 warnings)
- Tests: **OK** (72/72 passed)