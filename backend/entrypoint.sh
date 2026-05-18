#!/bin/sh
set -eu

: "${QWEN_VL_MODEL:=Qwen/Qwen3-VL-2B-Instruct}"
: "${QWEN_VL_DTYPE:=auto}"
: "${QWEN_VL_OCR_MAX_NEW_TOKENS:=80}"
: "${QWEN_VL_CHOICE_MAX_NEW_TOKENS:=12}"
: "${QWEN_VL_WARM_ON_START:=0}"
: "${HF_HUB_DISABLE_XET:=1}"
: "${GUNICORN_WORKERS:=1}"
: "${GUNICORN_THREADS:=2}"
: "${GUNICORN_TIMEOUT:=300}"
export QWEN_VL_MODEL
export QWEN_VL_DTYPE
export QWEN_VL_OCR_MAX_NEW_TOKENS
export QWEN_VL_CHOICE_MAX_NEW_TOKENS
export QWEN_VL_WARM_ON_START
export HF_HUB_DISABLE_XET
export GUNICORN_WORKERS
export GUNICORN_THREADS
export GUNICORN_TIMEOUT

if [ "$QWEN_VL_WARM_ON_START" = "1" ]; then
	python -c "from sync_api.services import warm_qwen_model; warm_qwen_model()"
fi

python manage.py migrate --noinput
exec gunicorn roster_sync.wsgi:application \
	--bind 0.0.0.0:8000 \
	--workers "$GUNICORN_WORKERS" \
	--threads "$GUNICORN_THREADS" \
	--timeout "$GUNICORN_TIMEOUT"