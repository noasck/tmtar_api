То что осталось по бэкенду:

-  [ ] M — add production logging [Read more...](https://docs.nginx.com/nginx/admin-guide/monitoring/logging/)
-  [x] M — add dependency injection for: fixtures, app, modules, service methods
-  [x] M — remove seeding database
-  [ ] M — add database backup and cache
-  [ ] M — add integration tests
-  [ ] M — add production tests
-  [ ] M — set up Profiling and Benchmark
-  [x] M — wsgi.py — add CLI commands and flask-migrate
-  [ ] M — config.py — add prod config as yml
-  [x] M — requirements — remove unused
-  [x] S — remove email hashing
-  [x] S — add relations between objects and fix tests
-  [ ] S — fix objects access
-  [x] D — add security headers (JWT) for flask_restx sqagger documentation
-  [ ] D — add validator for every field, validation exception handling, validation failing tests
-  [ ] D — add unique and other database exception handling
-  [ ] D — fix preferred event
-  [x] D — delete /user PUT route
-  [ ] D — add token expiration and JWT config.
-  [ ] D — provide auth0 authorization.
-  [ ] D — separate development\production auth.

_____________________________________________________
Закончить:

Event instance:
-  [ ] service
-  [ ] service tests
-  [ ] controller
-  [ ] controller tests

File instance:
-  [ ] controller tests

Zone:
-  [ ] configure PostGIS
-  [ ] model
-  [ ] interface
-  [ ] schemes
-  [ ] m, i, s tests
-  [ ] service
-  [ ] service tests
-  [ ] controller
-  [ ] controller tests

Subzone:
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

Большой блок:
Monitoring service — distinct project on Python. Features: tracking, logs gathering, status\retry tracker, Telegram notifications.
