/* the following are required for other container operations */
alter user postgres password 'PG_ROOT_PASSWORD';

create user PG_PRIMARY_USER with REPLICATION  PASSWORD 'PG_PRIMARY_PASSWORD';
create user PG_USER with password 'PG_PASSWORD';

create table primarytable (key varchar(20), value varchar(20));
grant all on primarytable to PG_PRIMARY_USER;

create database PG_DATABASE;
create database test;

grant all privileges on database PG_DATABASE to PG_USER;
grant all privileges on database test to PG_USER;

\c test

CREATE EXTENSION Postgis;
