#!/bin/bash
set -e
echo "Setting up PostgreSQL replication..."

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    DO \$\$
    BEGIN
        IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'replicator') THEN
            CREATE ROLE replicator WITH REPLICATION LOGIN PASSWORD 'repl_password_123';
        END IF;
    END
    \$\$;
EOSQL

# Add replication entry to pg_hba.conf
echo "host replication replicator 0.0.0.0/0 md5" >> "$PGDATA/pg_hba.conf"
echo "host replication all 0.0.0.0/0 md5" >> "$PGDATA/pg_hba.conf"

echo "PostgreSQL replication setup complete!"