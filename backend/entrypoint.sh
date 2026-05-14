#!/bin/sh
set -eu

: "${GEMINI_MODEL:=gemini-3-flash-preview}"
: "${GEMINI_WARM_ON_START:=0}"
: "${PORT:=8000}"
: "${GUNICORN_WORKERS:=1}"
: "${GUNICORN_TIMEOUT:=120}"
export GEMINI_MODEL
export GEMINI_WARM_ON_START
export PORT

if [ "$GEMINI_WARM_ON_START" = "1" ]; then
	python -c "from sync_api.services import warm_qwen_model; warm_qwen_model()"
fi

python manage.py migrate --noinput
exec gunicorn roster_sync.wsgi:application \
	--bind "0.0.0.0:${PORT}" \
	--workers "${GUNICORN_WORKERS}" \
	--timeout "${GUNICORN_TIMEOUT}"