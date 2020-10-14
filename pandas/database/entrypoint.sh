#!/bin/bash 

# Enable job control
set -m

# Based on: https://github.com/twright-msft/mssql-node-docker-demo-app

# Start SQL Server
/opt/mssql/bin/sqlservr & 

# Wait for the SQL Server to come up
echo RKO: Sleeping 30 sec start...
sleep 30s
echo RKO: Sleeping 30 sec end...

# Create the DB along with test data
echo RKO: Started executing sqlcmd script...
/opt/mssql-tools/bin/sqlcmd -U sa -P $SA_PASSWORD -d master \
    -i /usr/src/sql/create.sql
echo RKO: Finished executing sqlcmd script...

# Bring SQL Server to foreground
fg