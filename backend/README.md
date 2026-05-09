# Django Backend

This backend provides screenshot upload and roster recognition for the Vue frontend.

## What it does

- Accepts one or more roster screenshots through `POST /api/sync/recognize/`
- Detects identity cards inside each screenshot
- Uses a local `Qwen3-VL` model to read the identity name and level
- Uses frame-template matching plus border-pattern heuristics to estimate uptie
- Merges the detected values into the same roster shape used by the frontend local storage

## Requirements

- Python 3.11+
- Enough local CPU or GPU memory to run `Qwen3-VL`
- PostgreSQL reachable from Django if you run the backend outside Docker
- Network access the first time the model weights are downloaded from Hugging Face

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
set QWEN_VL_MODEL=Qwen/Qwen3-VL-2B-Instruct
set QWEN_VL_DTYPE=auto
python manage.py migrate
python manage.py runserver
```

## Docker

The Docker image installs a local `Qwen3-VL` runtime inside the backend container. You do not need any API key or OCR binary on your host machine.

`docker compose` builds the backend image with `torch` and `transformers`, mounts a persistent Hugging Face cache volume, and runs OCR through `Qwen/Qwen3-VL-2B-Instruct` by default.

The backend uses PostgreSQL in Docker. The compose file also starts a `postgres` service and mounts its data directory from an external Docker volume named `dantedoglcb-postgres-data`.

From the repository root:

```powershell
Copy-Item backend/.env.example .env
docker volume create dantedoglcb-postgres-data
docker compose up -d --build backend
```

The first OCR request downloads the model weights into the Docker volume `dantedoglcb-huggingface-cache`. If you want Docker to download the model immediately on startup, set `QWEN_VL_WARM_ON_START=1` in `.env` before running compose.

If your Docker host exposes an NVIDIA GPU, local `Qwen3-VL` inference is much faster with GPU acceleration. This workspace includes an optional [docker-compose.gpu.yml](docker-compose.gpu.yml) override:

```powershell
docker compose -f docker-compose.yml -f docker-compose.gpu.yml up -d --build backend
```

The current container environment may still run on CPU if no GPU is exposed to Docker. You can verify that inside the container with `python -c "import torch; print(torch.cuda.is_available())"`.

If you change the OCR packages or Dockerfile, rebuild with:

```powershell
docker compose build --no-cache backend
docker compose up backend
```

The container exposes the API on `http://127.0.0.1:8000`.

Inside the container, OCR runs through a local `Qwen3-VL` model and the image includes:

- `torch`
- `transformers`
- `accelerate`
- OpenCV runtime libraries

Default model:

- `Qwen/Qwen3-VL-2B-Instruct`

This default is the smallest open `Qwen3-VL` instruct checkpoint and is the most practical option for local Docker usage. CPU inference works but is slow; a CUDA GPU is strongly recommended for responsive OCR.

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