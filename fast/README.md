# Fast

Small FastAPI demo app ("Fastgram") with JWT auth, media uploads via ImageKit, and a minimal feed UI.

## Features
- JWT authentication, registration, password reset, and verification via `fastapi-users`
- Async SQLAlchemy models with SQLite (`test.db`)
- Image/video upload endpoint that stores media in ImageKit
- Feed endpoint with owner info and delete-by-owner support
- Static landing page served at `/` from `app/static`

## Project Layout
- `app/app.py` FastAPI app, routes, and static mounting
- `app/db.py` async SQLAlchemy models and session setup
- `app/users.py` auth backend and user manager
- `app/images.py` ImageKit client (env-driven)
- `app/static/index.html` simple UI
- `fast_api_notes/` notes (EN/中文) on FastAPI, SQLAlchemy, JWT, uploads, etc.
- `main.py` local dev runner

## Setup
1. Create a `.env` in `fast/` (or export env vars):
   - `IMAGEKIT_PRIVATE_KEY`
   - `IMAGEKIT_PUBLIC_KEY`
   - `IMAGEKIT_URL`
2. Install dependencies (example with uv):
   - `uv sync`

## Run
- `python main.py`
- or `uvicorn app.app:app --reload --host 0.0.0.0 --port 8000`

## API Quick Reference
- `GET /` static UI
- `POST /auth/jwt/login` login (JWT)
- `POST /auth/register` register
- `GET /users/me` current user
- `POST /upload` upload media (auth required, multipart: `file` + optional `caption`)
- `GET /feed` list posts (auth required)
- `DELETE /post/{post_id}` delete post (owner only)
- `GET /docs` interactive API docs

## Notes
- Database is SQLite at `fast/test.db` by default.
- Change `SECRET` in `app/users.py` for production use.
- FastAPI study notes live in `fast/fast_api_notes/`.
