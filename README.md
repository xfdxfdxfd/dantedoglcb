<div align="center">
<a href="https://github.com/xfdxfdxfd/dantedoglcb">
   <div style="max-width: 100%;height: auto;width: auto;"><img src="src/assets/DanteLogo.png"/></div>
</a>

# DanteDog

## FACE THE GRINDING, SAVE YOUR MONEY

### The all-in-one site for planning your future grinding

[![DanteDogGithub](https://img.shields.io/badge/DanteDog-Github-white)](https://github.com/xfdxfdxfd/dantedoglcb)
[![DanteDogDiscord](https://img.shields.io/badge/DanteDog-Discord-purple)](https://discord.gg/UdFrGmKfqE)

</div>

## Introduction

- Please be aware that this website is still under active developing.

  Its main purpose is to provide simple and reliable tools to faciliate your gameplay.

  Ensuring the accuracy of our tools is our top priority.

- Please use Google Chrome for the best experience

## What tools are included in this website

### Update Settings

- Set the status of your IDs and EGOs to update the information in all tools.

### Uptie Calculator

- Calculate the amount of threads and shards you need after setting the status in the "Update Settings"

### Level calculator

- Calculate the amount of exp you need for upgrading the ids

## Future plan

### Mirror Dungeon calculator

- Calculate the amount of md runs you need (and the resources you need) to get enough shards/threads

## License

- [![DanteDogLicense](https://img.shields.io/badge/DanteDog-License-green)](https://github.com/xfdxfdxfd/dantedoglcb/blob/master/LICENSE)

## Docker Compose

- `docker compose up --build` starts Postgres, Django on `http://127.0.0.1:8000`, and the Vite frontend on `http://127.0.0.1:5173`.
- Set `GOOGLE_OAUTH_CLIENT_ID` and `VITE_GOOGLE_CLIENT_ID` in `.env` to the same Google Web client ID.
- Add `http://127.0.0.1:5173` and `http://localhost:5173` to your Google OAuth Authorized JavaScript origins.

## Google Cloud Run

- The backend container now supports Cloud Run's `PORT` environment variable and Cloud SQL socket connections.
- Use [backend/.env.cloudrun.example](backend/.env.cloudrun.example) as the source of truth for backend runtime variables.
- Use [cloudbuild.yaml](cloudbuild.yaml) to build the backend image and deploy it to Cloud Run with a Cloud SQL PostgreSQL instance attached.
