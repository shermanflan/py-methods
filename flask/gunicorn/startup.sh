#!/bin/sh -eux

# Should generally set 2-4 workers per core
exec gunicorn \
  --workers=4 \
  --bind 0.0.0.0:5000 \
  --access-logfile - \
  --error-logfile - \
  "flask_methods:create_app()"