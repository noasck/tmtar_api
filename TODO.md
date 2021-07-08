## Backend


-  [x] M — add dependency injection for: fixtures, app, modules, service methods
-  [x] M — remove seeding database
-  [x] M — wsgi.py — add CLI commands and flask-migrate
-  [x] M — requirements — remove unused
-  [x] S — remove email hashing
-  [x] S — add relations between objects and fix tests
-  [x] D — add security headers (JWT) for flask_restX swagger documentation
-  [x] D — fix preferred event
-  [x] D — delete /user PUT route
-  [x] D — add token expiration and JWT config.
-  [x] D — provide auth0 authorization.
-  [x] D — separate development\production auth.
-  [ ] S — add database **migrations**.
-  [ ] M — add production logging [Read more...](https://docs.nginx.com/nginx/admin-guide/monitoring/logging/)
-  [ ] M — add database backup and cache
-  [ ] M — add integration tests
-  [ ] M — add production tests
-  [ ] M — set up Profiling and Benchmark
-  [ ] M — config.py — add prod config as yml
-  [ ] S — fix objects access
-  [ ] D — add validator for every field, validation exception handling, validation failing tests
-  [ ] D — add unique and other database exception handling
-  [ ] D — add OpenStreetMap, auto country detect for zones
_____________________________________________________
## Finish ASAP

### Event instance:
-  [x] service
-  [x] service tests
-  [x] controller
-  [x] controller tests

### File instance:
-  [ ] controller tests


### Zone:

-  [x] configure PostGIS
-  [x] model
-  [x] interface
-  [x] schemes
-  [x] m, i, s tests
-  [x] service
-  [x] service tests
-  [ ] controller
-  [ ] controller tests

### Subzone:

-  [ ] model
-  [ ] interface
-  [ ] schemes
-  [ ] m, i, s tests
-  [ ] service
-  [ ] service tests
-  [ ] controller
-  [ ] controller tests
-  [ ] object relation
-  [ ] object integration tests

**Monitoring service** — distinct project on Python. Features: tracking, logs gathering, status\retry tracker, Telegram notifications.
