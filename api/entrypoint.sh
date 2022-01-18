#!/bin/bash

set -e

pushd models/migrations
alembic upgrade head
popd

exec gunicorn -b 0.0.0.0:3001 --worker-class gevent app:app "$@"
