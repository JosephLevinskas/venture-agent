# VentureAgent

`VentureAgent` is a full-stack AI research agent project. The goal is to build a backend-first application that can manage research projects, store documents/notes, and later use retrieval, embeddings, and LLMs to generate structured research reports.

This repo is being built as a 14-day project sprint to learn backend engineering, databases, Docker, full-stack development, and deployment patterns.

## Current Status

Day 1, Day 2, and Day 3 are complete.

The project currently has:

* A FastAPI backend.
* A PostgreSQL database running through Docker Compose.
* SQLAlchemy database setup.
* A working `Project` database model.
* Pydantic schemas for request/response validation.
* Full CRUD API routes for projects.
* Swagger/OpenAPI docs available at `/docs`.

No frontend has been implemented yet.

---

## Tech Stack

### Backend

* Python 3.12
* FastAPI
* Uvicorn
* SQLAlchemy
* Pydantic
* psycopg2-binary
* python-dotenv

### Database

* PostgreSQL 16
* Docker volume for persistent database storage

### DevOps / Tooling

* Docker
* Docker Compose
* Git / GitHub

### Planned Later

* React + TypeScript frontend
* Authentication with JWT (basic implemented)
* Document storage
* Embeddings / vector search
* RAG question answering
* Research memo generation
* Tests and GitHub Actions CI
* Deployment
* Kubernetes / Terraform basics

---

## Project Structure

```txt
venture-agent/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── database.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   └── routers/
│   │       ├── __init__.py
│   │       └── projects.py
│   ├── tests/
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
├── infra/
├── docs/
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md
```

---

## What I Built on Day 1

Day 1 focused on setting up the project foundation.

Completed:

* Created the main project structure:

	* `backend/`
	* `frontend/`
	* `infra/`
	* `docs/`
* Initialized Git and pushed the repo to GitHub.
* Created a minimal FastAPI backend.
* Added a `/health` endpoint.
* Created `backend/requirements.txt`.
* Created a backend `Dockerfile`.
* Created `docker-compose.yml`.
* Added a PostgreSQL service using the official `postgres:16` Docker image.
* Added a persistent Docker volume for Postgres data.
* Added `.env`, `.env.example`, and `.gitignore`.
* Learned the difference between:

	* Dockerfile
	* Docker image
	* Docker container
	* Docker Compose service
	* Docker volume
* Verified the backend could run locally and through Docker.

The initial health endpoint:

```txt
GET /health
```

returns:

```json
{
	"status": "ok"
}
```

---

## What I Built on Day 2

Day 2 focused on making the backend store and manage real data.

The first real domain object is `Project`.

A project is the top-level object because future documents, chunks, reports, scores, and AI outputs will belong to a project.

Completed:

* Added SQLAlchemy database setup in:

```txt
backend/app/database.py
```

* Added:

	* `DATABASE_URL`
	* SQLAlchemy engine
	* session factory
	* declarative `Base`
	* `get_db()` dependency for FastAPI routes

* Added a `Project` model in:

```txt
backend/app/models.py
```

The `Project` table includes:

* `id`

* `title`

* `description`

* `created_at`

* `updated_at`

* Added Pydantic schemas in:

```txt
backend/app/schemas.py
```

Schemas:

* `ProjectBase`

* `ProjectCreate`

* `ProjectUpdate`

* `ProjectRead`

* Added project routes in:

```txt
backend/app/routers/projects.py
```

Current project API routes:

```txt
POST   /projects
GET    /projects
GET    /projects/{project_id}
PATCH  /projects/{project_id}
DELETE /projects/{project_id}
```

---

## API Endpoints

### Health Check

```txt
GET /health
```

Example response:

```json
{
	"status": "ok"
}
```

---

### Create Project

```txt
POST /projects
```

Example request:

```json
{
	"title": "First Research Project",
	"description": "Testing project creation through the API"
}
```

Example response:

```json
{
	"title": "First Research Project",
	"description": "Testing project creation through the API",
	"id": 1,
	"created_at": "2026-06-10T17:00:00Z",
	"updated_at": "2026-06-10T17:00:00Z"
}
```

---

### List Projects

```txt
GET /projects
```

Example response:

```json
[
	{
		"title": "First Research Project",
		"description": "Testing project creation through the API",
		"id": 1,
		"created_at": "2026-06-10T17:00:00Z",
		"updated_at": "2026-06-10T17:00:00Z"
	}
]
```

---

### Get One Project

```txt
GET /projects/{project_id}
```

Example:

```txt
GET /projects/1
```

If the project exists, it returns that project.

If it does not exist, it returns:

```json
{
	"detail": "Project not found"
}
```

---

### Update Project

```txt
PATCH /projects/{project_id}
```

Example request:

```json
{
	"description": "Updated project description"
}
```

This route supports partial updates, so the caller can update only `title`, only `description`, or both.

---

### Delete Project

```txt
DELETE /projects/{project_id}
```

Example response:

```json
{
	"message": "Project deleted successfully"
}
```


## Day 3 — Authentication Basics

Added basic user authentication support.

### Completed

- Added `User` SQLAlchemy model.
- Created `users` table in PostgreSQL.
- Added Pydantic schemas:
	- `UserCreate`
	- `UserLogin`
	- `UserRead`
	- `Token`
- Added password hashing with `pwdlib[argon2]`.
- Added JWT creation and decoding with `PyJWT`.
- Added auth routes:
	- `POST /auth/register`
	- `POST /auth/login`
	- `GET /auth/me`
- Added reusable auth dependency:
	- `get_current_user`
- Added automated tests for:
	- user registration
	- duplicate email handling
	- hashed password storage
	- login success
	- login failure
	- JWT token response
	- `/auth/me` with and without token

### Auth Flow

1. User registers with email and password.
2. Backend hashes the password before saving it.
3. User logs in with email and password.
4. Backend verifies the password against the stored hash.
5. Backend returns a JWT access token.
6. Protected routes can use the token to identify the current user.

### Current Auth Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/auth/register` | Create a new user |
| `POST` | `/auth/login` | Log in and receive a JWT |
| `GET` | `/auth/me` | Return the current logged-in user |


## How to Run Locally

### 1. Create and activate a virtual environment

From the project root:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install backend dependencies

```bash
pip install -r backend/requirements.txt
```

### 3. Create local environment file

Copy the example environment file:

```bash
cp .env.example .env
```

Example `.env` values:

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=venture_agent
DATABASE_URL=postgresql://postgres:postgres@127.0.0.1:5433/venture_agent
```

Do not commit `.env`.

---

## Running with Docker Compose

Start the backend and Postgres:

```bash
docker compose up -d --build
```

Check running containers:

```bash
docker compose ps
```

Expected services:

```txt
backend
postgres
```

The backend should be available at:

```txt
http://localhost:8000
```

Swagger/OpenAPI docs:

```txt
http://localhost:8000/docs
```

Health endpoint:

```txt
http://localhost:8000/health
```

---

## Running the Backend Locally Without Docker

Postgres should still be running through Docker Compose:

```bash
docker compose up -d postgres
```

Then run the backend locally from the project root:

```bash
PYTHONPATH=backend uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Why `PYTHONPATH=backend` is needed:

The backend code imports modules like:

```python
from app.database import Base
```

So Python needs to know that `backend/` is the folder where the `app` package lives.

---

## Database Notes

The project uses PostgreSQL through Docker Compose.

In `docker-compose.yml`, Postgres maps:

```txt
5433:5432
```

Meaning:

```txt
host machine port 5433 -> Postgres container port 5432
```

So when running Python directly on the Mac, the database URL uses:

```txt
127.0.0.1:5433
```

Example:

```env
DATABASE_URL=postgresql://postgres:postgres@127.0.0.1:5433/venture_agent
```

Inside Docker Compose, the backend container talks to Postgres using the Compose service name:

```txt
postgres:5432
```

That is configured in `docker-compose.yml` under the backend service:

```yaml
environment:
	DATABASE_URL: postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@postgres:5432/${POSTGRES_DB}
```

Important idea:

```txt
Mac Python uses:        127.0.0.1:5433
Docker backend uses:    postgres:5432
```

Both point to the same Postgres database, but from different network locations.

---

## Useful Commands

Start all services:

```bash
docker compose up -d --build
```

Stop services:

```bash
docker compose down
```

Stop services and delete database volume:

```bash
docker compose down -v
```

Warning: `docker compose down -v` deletes the Postgres volume and destroys local database data.

View backend logs:

```bash
docker compose logs backend --tail=80
```

View Postgres logs:

```bash
docker compose logs postgres --tail=80
```

Open Postgres shell:

```bash
docker compose exec postgres psql -U postgres -d venture_agent
```

Inside `psql`, list tables:

```sql
\dt
```

Describe the projects table:

```sql
\d projects
```

Exit `psql`:

```sql
\q
```

---

## Example Curl Commands

Create a project:

```bash
curl -X POST "http://localhost:8000/projects" \
	-H "Content-Type: application/json" \
	-d '{"title":"My project","description":"notes"}'
```

List projects:

```bash
curl "http://localhost:8000/projects"
```

Get one project:

```bash
curl "http://localhost:8000/projects/1"
```

Update a project:

```bash
curl -X PATCH "http://localhost:8000/projects/1" \
	-H "Content-Type: application/json" \
	-d '{"title":"Updated title"}'
```

Delete a project:

```bash
curl -X DELETE "http://localhost:8000/projects/1"
```

---

## Troubleshooting

### `password authentication failed for user "postgres"`

This usually means the Postgres volume was initialized with old credentials.

If it is okay to delete local database data, reset with:

```bash
docker compose down -v
docker compose up -d --build
```

### `DATABASE_URL is not set`

The backend container needs its own `DATABASE_URL` in `docker-compose.yml`.

Make sure the backend service has:

```yaml
environment:
	DATABASE_URL: postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@postgres:5432/${POSTGRES_DB}
```

### `connection refused`

This usually means Postgres is not running.

Check:

```bash
docker compose ps
```

Then start services:

```bash
docker compose up -d
```

### Route exists in file but not in `/docs`

Make sure the router is included in `main.py`:

```python
from app.routers import projects

app.include_router(projects.router)
```

---

## What I Am Learning

This project is teaching:

* How to structure a backend project.
* How FastAPI routes work.
* How Uvicorn serves a FastAPI app.
* How Docker images and containers work.
* How Docker Compose runs multiple services.
* How Postgres stores application data.
* How SQLAlchemy maps Python classes to database tables.
* How Pydantic validates API input and output.
* How environment variables configure apps.
* How local development differs from containerized development.
* How to build CRUD routes step by step.

---

## Next Steps

Day 3 will add authentication.

Planned Day 3 work:

* Add a `User` model.
* Create a `users` table.
* Add password hashing.
* Add registration route.
* Add login route.
* Add JWT token generation.
* Connect projects to users later so each user owns their own projects.

Later milestones:

* React + TypeScript frontend.
* Document upload/notes system.
* Chunking and embeddings.
* RAG search over project documents.
* AI-generated research memos.
* Tests and GitHub Actions CI.
* Deployment.
* Kubernetes and Terraform basics.
