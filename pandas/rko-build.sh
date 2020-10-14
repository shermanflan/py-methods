#!/bin/bash -eux

docker container prune -f
docker image prune -f

docker image rm sql-fabulous || echo 'sql-fabulous does not exist...'
docker image rm python-heinous || echo 'python-heinous does not exist...'

docker-compose build