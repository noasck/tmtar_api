#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$PG_USER" --dbname "$PG_DATABASE" <<-EOSQL
    CREATE DATABASE tmtar_test;
EOSQL