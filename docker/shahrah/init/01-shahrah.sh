#!/bin/sh
# Runs once on an empty data directory (docker-entrypoint-initdb.d).
# Creates the role shahrah logs in as and the function it reads SCRAM verifiers
# through — shahrah never sees a client password in the clear.
set -eu
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname postgres \
     -v pw="$SHAHRAH_BACKEND_PASSWORD" <<'SQL'
create role shahrah login superuser password :'pw';
create or replace function shahrah_get_auth(in wanted text,
                                            out username text, out verifier text)
returns record as $$
  select rolname::text, rolpassword::text from pg_authid where rolname = $1
$$ language sql security definer;
revoke all on function shahrah_get_auth(text) from public;
SQL
