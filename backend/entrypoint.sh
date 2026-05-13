#!/bin/sh
set -eu

: "${GEMINI_MODEL:=gemini-3-flash-preview}"
: "${GEMINI_WARM_ON_START:=0}"
export GEMINI_MODEL
export GEMINI_WARM_ON_START

if [ "$GEMINI_WARM_ON_START" = "1" ]; then
	python -c "from sync_api.services import warm_qwen_model; warm_qwen_model()"
fi

python manage.py migrate --noinput
exec python manage.py runserver 0.0.0.0:8000