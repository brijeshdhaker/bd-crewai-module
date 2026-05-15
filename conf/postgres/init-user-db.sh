#!/usr/bin/env bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
	CREATE USER pgadmin;
	CREATE DATABASE SANDBOXDB;
	GRANT ALL PRIVILEGES ON DATABASE SANDBOXDB TO pgadmin;
	GRANT CONNECT ON DATABASE SANDBOXDB TO pgadmin;
	GRANT USAGE ON SCHEMA public TO pgadmin;
	-- Grant read access to all existing tables
	GRANT SELECT ON ALL TABLES IN SCHEMA public TO pgadmin;
	-- Grant full access to all existing tables
	GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO pgadmin;
EOSQL

psql -U postgres -tc "SELECT 1 FROM pg_database WHERE datname = 'my_db_name'" | grep -q 1 || psql -U postgres -c "CREATE DATABASE my_db_name"

DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_database WHERE datname = 'my_db_name') THEN
        PERFORM dblink_exec('dbname=postgres', 'CREATE DATABASE my_db_name');
    END IF;
END $$;


sudo -u postgres psql -c 'SHOW hba_file;'