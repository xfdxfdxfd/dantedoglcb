#!/bin/sh
set -eu

: "${QWEN_VL_MODEL:=Qwen/Qwen3-VL-2B-Instruct}"
: "${QWEN_VL_WARM_ON_START:=0}"
export QWEN_VL_MODEL
export QWEN_VL_WARM_ON_START

if [ "$QWEN_VL_WARM_ON_START" = "1" ]; then
	python -c "from sync_api.services import warm_qwen_model; warm_qwen_model()"
fi

python manage.py migrate --noinput
exec python manage.py runserver 0.0.0.0:8000