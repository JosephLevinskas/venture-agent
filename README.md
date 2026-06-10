# Venture Agent

Short experimental project exploring autonomous/assistant agents and deployment patterns.

## Description

`Venture Agent` is a small learning project that explores building a minimal backend API for an agent-style application, containerized deployment, and the developer workflow around iteration and documentation. The current codebase contains a minimal FastAPI backend and placeholders for frontend and infra.

## What I'm learning

- Building a lightweight API with `FastAPI` and `uvicorn`.
- How to structure a small project with separate `backend/`, `frontend/`, and `infra/` folders.
- Containerizing services using `Docker` and `docker-compose`.
- Iterative development: small, testable endpoints and clear README/run instructions.

## Current status

- Day 1 (initial): repository scaffolded. Minimal health endpoint implemented in the backend. Basic project structure in place.
- No frontend app yet; infra and docs folders created for future work.

## What I did today (Day 1)

- Created repository skeleton with these top-level folders: `backend/`, `frontend/`, `infra/`, `docs/`, `tests/`.
- Implemented a minimal FastAPI app at `backend/app/main.py` with a `/health` endpoint.
- Added `backend/requirements.txt` listing `fastapi` and `uvicorn`.
- Added a `Dockerfile` and `docker-compose.yml` placeholders for future containerized runs.
- Drafted this `README.md` to capture the goals and local run instructions.

## Tech stack

- Python 3.x
- FastAPI (backend)
- Uvicorn (ASGI server)
- Docker & Docker Compose (containerization)
- (future) Frontend: TBD

## How to run locally

1. Create a Python virtual environment and install backend requirements:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
```

2. Run the FastAPI app with Uvicorn (development):

```bash
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```

3. Alternatively, build and run with Docker Compose (if Docker is installed):

```bash
docker-compose up --build
```

## What site to visit

- API root (OpenAPI docs): http://localhost:8000/docs
- Health endpoint: http://localhost:8000/health

If you run via Docker Compose and ports are different, check your `docker-compose.yml` mapping.

## Next steps

- Add more backend endpoints and unit tests (expand `tests/`).
- Implement a frontend app in `frontend/` and wire it to the API.
- Add CI (GitHub Actions) to run tests and linting.
- Add a proper `LICENSE` file (MIT recommended).

