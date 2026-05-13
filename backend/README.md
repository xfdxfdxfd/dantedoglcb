# Django Backend

This backend provides screenshot upload and roster recognition for the Vue frontend.

## What it does

- Accepts one or more roster screenshots through `POST /api/sync/recognize/`
- Detects identity cards inside each screenshot
- Uses Google `Gemini 3 Flash` to read the identity name and level
- Uses frame-template matching plus border-pattern heuristics to estimate uptie
- Merges the detected values into the same roster shape used by the frontend local storage

## Requirements

- Python 3.11+
- A valid Gemini API key
- PostgreSQL reachable from Django if you run the backend outside Docker
- Network access from the backend to the Gemini API

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
set GEMINI_API_KEY=your-api-key
set GEMINI_MODEL=gemini-3-flash-preview
python manage.py migrate
python manage.py runserver
```

## Docker

The backend now calls the Gemini API from inside the container. You do not need a local OCR model on your host machine, but you do need `GEMINI_API_KEY` set in your environment or `.env` file.

`docker compose` builds the backend image with the Google GenAI SDK and runs OCR through `gemini-3-flash-preview` by default.

The backend uses PostgreSQL in Docker. The compose file also starts a `postgres` service and mounts its data directory from an external Docker volume named `dantedoglcb-postgres-data`.

From the repository root:

```powershell
Copy-Item backend/.env.example .env
docker volume create dantedoglcb-postgres-data
docker compose up -d --build backend
```

If you want the container to validate Gemini client initialization on startup, set `GEMINI_WARM_ON_START=1` in `.env` before running compose.

If your Docker host exposes an NVIDIA GPU, this workspace still includes an optional [docker-compose.gpu.yml](docker-compose.gpu.yml) override, but Gemini OCR itself runs through the remote Gemini API rather than local GPU inference:

```powershell
docker compose -f docker-compose.yml -f docker-compose.gpu.yml up -d --build backend
```

The backend container no longer depends on `torch` or `transformers` for OCR.

If you change the OCR packages or Dockerfile, rebuild with:

```powershell
docker compose build --no-cache backend
docker compose up backend
```

The container exposes the API on `http://127.0.0.1:8000`.

Inside the container, OCR runs through the Gemini API and the image includes:

- `google-genai`
- OpenCV runtime libraries

Default model:

- `gemini-3-flash-preview`

This default is Google's Gemini 3 Flash preview model. The backend sends image bytes and prompts to the Gemini API, so runtime speed depends on API latency rather than local model loading.

If you want to override Django settings, copy `backend/.env.example` values into your shell environment or repository-root `.env` file before starting compose.

## Debugging OCR

For faster OCR tuning on real screenshots, use the Django management command below. It prints one detected card at a time and can optionally write each crop plus a JSON report to disk.

```powershell
docker compose exec backend python manage.py debug_cards /app/test_image/testimg2.png --output-dir /app/debug_cards
```

## Optional frame templates

For more accurate uptie detection, add sample frame crops into:

- `sync_api/frame_templates/uptie1/`
- `sync_api/frame_templates/uptie2/`
- `sync_api/frame_templates/uptie3/`
- `sync_api/frame_templates/uptie4/`

PNG or JPG files are supported. The recognizer falls back to heuristics when no templates are present.