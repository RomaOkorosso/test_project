#!/bin/bash

if [ "$DATABASE" = "postgres" ]; then
  until
    export PGPASSWORD=$POSTGRES_PASSWORD
    # shellcheck disable=SC2086
    psql -h $POSTGRES_HOST -p 5432 -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "select 1" >/dev/null 2>&1
  do
    echo "Waiting for postgres server"
    sleep 1
  done

  echo "PostgreSQL started"
fi

alembic upgrade head

exec "$@"
