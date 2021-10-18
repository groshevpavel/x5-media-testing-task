#! /usr/bin/env sh

sleep 5

cd /opt/x5-test/
alembic upgrade head
cd /app
