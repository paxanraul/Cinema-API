#!/bin/sh
echo "Применение миграций..."
alembic upgrade head
uvicorn main:app --host 0.0.0.0 