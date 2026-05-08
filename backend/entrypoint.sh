#!/bin/sh
set -eu

: "${TESSERACT_CMD:=/usr/bin/tesseract}"
: "${TESSDATA_PREFIX:=/usr/share/tesseract-ocr/5/tessdata}"
export TESSERACT_CMD
export TESSDATA_PREFIX

if [ ! -x "$TESSERACT_CMD" ]; then
	echo "Tesseract executable not found at $TESSERACT_CMD" >&2
	exit 1
fi

"$TESSERACT_CMD" --version >/dev/null 2>&1

python manage.py migrate --noinput
exec python manage.py runserver 0.0.0.0:8000