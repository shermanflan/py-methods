#!/bin/bash -eux

docker-compose build

docker-compose run python-heinous /bin/bash