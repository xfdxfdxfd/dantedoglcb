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

## Runtime spec

- GPU is not required. Gemini OCR runs against the remote Gemini API, so the optional GPU compose override is not needed for recognition quality or throughput.
- Local Docker baseline: 2 vCPU and 4 GB RAM is enough to run one backend worker plus PostgreSQL for single-user testing.
- Local recommended headroom: 4 vCPU and 8 GB RAM if you want faster screenshot turnaround, rebuilds, or multiple screenshots queued back to back.
- Cloud Run production default in this repo: 4 vCPU, 8 GiB RAM, concurrency 1, Cloud Run request timeout `300s`, `GUNICORN_WORKERS=1`, and `GUNICORN_TIMEOUT=300`.
- Network stability matters more than GPU. The heavy OCR work is remote API latency, while local CPU/RAM mainly cover OpenCV preprocessing, image assembly, and Django.

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
gunicorn roster_sync.wsgi:application --bind 0.0.0.0:8000
```

## Docker

The backend now calls the Gemini API from inside the container. You do not need a local OCR model on your host machine, but you do need `GEMINI_API_KEY` set in your environment or `.env` file.

`docker compose` builds the backend image with the Google GenAI SDK and serves Django through `gunicorn` on port `8000` by default while running OCR through `gemini-3-flash-preview`.

To reduce Gemini OCR call count per screenshot, the backend batches multiple detected cards into one OCR request by default. Set `GEMINI_BATCH_OCR_MAX_CARDS_PER_CALL=6` to control how many cards are grouped into one Gemini call. The batch OCR path also defaults `GEMINI_BATCH_OCR_THINKING_BUDGET=0` so Gemini spends output tokens on the returned card blocks instead of hidden reasoning. For example, a 12-card screenshot now targets about 2 Gemini OCR calls instead of 12, while `GEMINI_NAME_CHOICE_MAX_CALLS_PER_SCREENSHOT=1` still caps the more expensive ambiguity fallback.

The backend now defaults `GEMINI_UPTIE_MAX_CALLS_PER_SCREENSHOT=0`, which disables the last Gemini uptie fallback by default. That keeps recognition on the batched OCR path plus local frame heuristics, which is materially faster on Cloud Run and avoids slipping over a 30-second worker timeout.

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

## Cloud Run

The Docker Compose default `POSTGRES_HOST=postgres` only works inside the local Compose network. On Cloud Run, configure the database explicitly so Django does not fall back to that hostname.

Set `POSTGRES_HOST` to the Cloud SQL Unix socket path and keep the regular PostgreSQL credentials in the other variables.

Example Cloud Run environment variables for Cloud SQL PostgreSQL:

```text
POSTGRES_HOST=/cloudsql/your-project:your-region:your-instance
POSTGRES_DB=dantedoglcb
POSTGRES_USER=dantedoglcb
POSTGRES_PASSWORD=change-me
DJANGO_ALLOWED_HOSTS=your-service-xxxx.a.run.app
DJANGO_DEBUG=false
GEMINI_API_KEY=your-api-key
```

Required runtime environment variables for Cloud Run:

```text
DJANGO_DEBUG=false
DJANGO_SECRET_KEY=replace-with-a-secret-manager-value
DJANGO_ALLOWED_HOSTS=your-service-xxxx.a.run.app
POSTGRES_HOST=/cloudsql/your-project:your-region:your-instance
POSTGRES_DB=dantedoglcb
POSTGRES_USER=dantedoglcb
POSTGRES_PASSWORD=replace-with-a-secret-manager-value
GEMINI_API_KEY=replace-with-a-secret-manager-value
GEMINI_MODEL=gemini-3-flash-preview
GEMINI_MAX_NEW_TOKENS=192
GEMINI_BATCH_OCR_MAX_CARDS_PER_CALL=6
GEMINI_BATCH_OCR_MAX_NEW_TOKENS=640
GEMINI_BATCH_OCR_THINKING_BUDGET=0
GEMINI_WARM_ON_START=0
GEMINI_NAME_CHOICE_MAX_CALLS_PER_SCREENSHOT=1
GEMINI_UPTIE_MAX_CALLS_PER_SCREENSHOT=0
GUNICORN_WORKERS=1
GUNICORN_TIMEOUT=300
GOOGLE_OAUTH_CLIENT_IDS=your-google-web-client-id
```

Backend-relevant Cloud Run environment variables from your current service setup are the Django, PostgreSQL, Google OAuth, Gemini, and Gunicorn settings above. The backend does not currently read `VITE_API_BASE_URL`, `VITE_GOOGLE_CLIENT_ID`, `CHOKIDAR_USEPOLLING`, `SCREENSHOT_REGION_MAX_PREVIEW_DIMENSION`, `SCREENSHOT_REGION_BOX_PADDING`, or `LOCAL_SCREENSHOT_REGION_FALLBACK`, so keeping those in the Cloud Run UI is harmless but they are not part of the backend deploy contract.

Optional runtime environment variables:

```text
GOOGLE_OAUTH_CLIENT_ID=your-google-web-client-id
GEMINI_UPTIE_MAX_CALLS_PER_SCREENSHOT=1
```

Cloud Run sets `PORT` automatically. The container entrypoint now binds Gunicorn to that port.

`cloudbuild.yaml` now deploys Cloud Run with explicit `--command=/app/entrypoint.sh`, `--cpu`, `--memory`, `--concurrency`, and `--timeout` flags so the production service uses the repository entrypoint and matches the documented runtime spec instead of inheriting older service defaults.

`cloudbuild.yaml` also now sets `POSTGRES_HOST=/cloudsql/${_CLOUD_SQL_INSTANCE}` during deploy, which matches the Cloud Run environment value you listed for the Cloud SQL Unix socket path.

If your frontend is deployed separately, build it with:

```text
VITE_API_BASE_URL=https://your-backend-service-xxxx.a.run.app
VITE_GOOGLE_CLIENT_ID=your-google-web-client-id
```

If you deploy through Cloud Build, the repository root now includes `cloudbuild.yaml` for building the backend image and deploying it to Cloud Run with Cloud SQL attached.

Cloud Build expects these Secret Manager secrets to exist:

```text
django-secret-key
postgres-password
gemini-api-key
```

Cloud Build substitutions you should update before the first deploy:

```text
_SERVICE_NAME
_REGION
_ARTIFACT_REPOSITORY
_CLOUD_SQL_INSTANCE
_POSTGRES_DB
_POSTGRES_USER
_DJANGO_ALLOWED_HOSTS
_GOOGLE_OAUTH_CLIENT_ID
_GOOGLE_OAUTH_CLIENT_IDS
_CPU
_MEMORY
_CONCURRENCY
_REQUEST_TIMEOUT
_GEMINI_MODEL
_GEMINI_BATCH_OCR_MAX_CARDS_PER_CALL
_GEMINI_BATCH_OCR_MAX_NEW_TOKENS
_GEMINI_BATCH_OCR_THINKING_BUDGET
_GEMINI_NAME_CHOICE_MAX_CALLS_PER_SCREENSHOT
_GEMINI_UPTIE_MAX_CALLS_PER_SCREENSHOT
_GUNICORN_WORKERS
_GUNICORN_TIMEOUT
```

Example deploy command:

```powershell
gcloud builds submit --config cloudbuild.yaml \
	--substitutions=_SERVICE_NAME=dantedoglcb-backend,_REGION=us-central1,_ARTIFACT_REPOSITORY=dantedoglcb,_CLOUD_SQL_INSTANCE=your-project:your-region:your-instance,_POSTGRES_DB=dantedoglcb,_POSTGRES_USER=dantedoglcb,_DJANGO_ALLOWED_HOSTS=your-service-xxxx.a.run.app,_GOOGLE_OAUTH_CLIENT_ID=your-google-web-client-id,_GOOGLE_OAUTH_CLIENT_IDS=your-google-web-client-id
```

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