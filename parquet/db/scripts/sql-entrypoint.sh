#!/bin/bash

# Enable job control
set -m

# Based on: https://github.com/twright-msft/mssql-node-docker-demo-app

echo 'Starting SQL Server...'

/opt/mssql/bin/sqlservr &

sleep 30s

echo 'Running creation script...'

/opt/mssql-tools/bin/sqlcmd -U sa -P $SA_PASSWORD -d master \
    -i $APP_HOME/scripts/db_create.sql

wait