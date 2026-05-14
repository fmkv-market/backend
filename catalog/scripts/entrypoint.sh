#!/bin/sh
backend() {
  echo "Start server"
  sleep 5
  if command -v alembic >/dev/null 2>&1; then
    if [ -f "/opt/alembic.ini" ]; then
      alembic -c /opt/alembic.ini upgrade head
    elif [ -f "alembic.ini" ]; then
      alembic -c alembic.ini upgrade head
    else
      echo "Skip migrations: alembic.ini not found"
    fi
  fi
  uvicorn myapp.main:app --proxy-headers --host 0.0.0.0 --port 8002 --reload
}
$1