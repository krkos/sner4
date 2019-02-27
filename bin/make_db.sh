#!/bin/sh
set -e

BASE="$(readlink -f $(dirname $(readlink -f $0))/..)"

export SNER_CONFIG="${BASE}/sner_web.cfg"

#su -c 'psql --command="CREATE ROLE root WITH LOGIN;"' postgres
#su -c 'psql --command="CREATE DATABASE sner OWNER root;"' postgres
psql --command="SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname='sner';" postgres
psql -t --command="SELECT 'drop table '||tablename||' cascade;' FROM pg_tables WHERE schemaname='public';" sner | psql sner

export FLASK_APP="sner_web"
flask sner_init_db
flask sner_init_data
