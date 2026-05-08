# Django Backend

This backend provides screenshot upload and roster recognition for the Vue frontend.

## What it does

- Accepts one or more roster screenshots through `POST /api/sync/recognize/`
- Detects identity cards inside each screenshot
- Uses OCR to read the identity name and level
- Uses frame-template matching plus border-pattern heuristics to estimate uptie
- Merges the detected values into the same roster shape used by the frontend local storage

## Requirements

- Python 3.11+
- Tesseract OCR installed on the machine only if you run Django outside Docker
- PostgreSQL reachable from Django if you run the backend outside Docker

If Tesseract is not on `PATH`, set `TESSERACT_CMD` before starting Django.

## Install

```powershell
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
set POSTGRES_HOST=127.0.0.1
set POSTGRES_PORT=5432
set POSTGRES_DB=dantedoglcb
set POSTGRES_USER=dantedoglcb
set POSTGRES_PASSWORD=change-me
python manage.py migrate
python manage.py runserver
```

## Docker

The Docker image hosts Tesseract OCR inside the backend container. You do not need Tesseract installed on your host machine when using Docker.

`docker compose` builds the backend image with Tesseract already installed and starts the container with `TESSERACT_CMD=/usr/bin/tesseract` and `TESSDATA_PREFIX=/usr/share/tesseract-ocr/5/tessdata`.

The backend uses PostgreSQL in Docker. The compose file also starts a `postgres` service and mounts its data directory from an external Docker volume named `dantedoglcb-postgres-data`.

From the repository root:

```powershell
docker volume create dantedoglcb-postgres-data
docker compose up --build backend
```

If you change the OCR packages or Dockerfile, rebuild with:

```powershell
docker compose build --no-cache backend
docker compose up backend
```

The container exposes the API on `http://127.0.0.1:8000`.

Inside the container, OCR runs through `/usr/bin/tesseract` and the image includes:

- `tesseract-ocr`
- `tesseract-ocr-eng`
- `tesseract-ocr-osd`

If you want to override Django settings, copy `backend/.env.example` values into your shell environment before starting compose.

## Optional frame templates

For more accurate uptie detection, add sample frame crops into:

- `sync_api/frame_templates/uptie1/`
- `sync_api/frame_templates/uptie2/`
- `sync_api/frame_templates/uptie3/`
- `sync_api/frame_templates/uptie4/`

PNG or JPG files are supported. The recognizer falls back to heuristics when no templates are present.