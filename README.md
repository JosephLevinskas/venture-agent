# VentureAgent

`VentureAgent` is a full-stack AI research agent project. The goal is to build a backend-first application that can manage research projects, store documents/notes, and later use retrieval, embeddings, and LLMs to generate structured research reports.

This repo is being built as a 14-day project sprint to learn backend engineering, databases, Docker, authentication, full-stack development, testing, CI, and deployment patterns.

---

## Current Status

Day 1, Day 2, Day 3, and Day 4 are complete.

The project currently has:

* A FastAPI backend.
* A PostgreSQL database running through Docker Compose.
* SQLAlchemy database setup.
* A working `User` database model.
* A working `Project` database model.
* A foreign-key relationship from projects to users.
* Pydantic schemas for request/response validation.
* User registration and login.
* Password hashing with Argon2.
* JWT access token creation and decoding.
* A reusable `get_current_user` dependency.
* Protected project CRUD routes.
* User-owned projects, meaning each project belongs to the logged-in user.
* Automated backend tests with `pytest` and FastAPI `TestClient`.
* Swagger/OpenAPI docs available at `/docs`.

No frontend has been implemented yet.

Important current limitation:

* Alembic migrations are not implemented yet.
* During development, schema changes may require resetting the local Postgres volume with `docker compose down -v`.

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
* pwdlib[argon2]
* PyJWT

### Database

* PostgreSQL 16
* Docker volume for persistent database storage

### Testing

* pytest
* FastAPI TestClient
* Temporary SQLite test database

### DevOps / Tooling

* Docker
* Docker Compose
* Git / GitHub

### Planned Later

* Alembic database migrations
* React + TypeScript frontend
* Document storage
* Embeddings / vector search
* RAG question answering
* Research memo generation
* GitHub Actions CI
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
│   │   ├── security.py
│   │   ├── dependencies.py
│   │   └── routers/
│   │       ├── __init__.py
│   │       ├── auth.py
│   │       └── projects.py
│   ├── tests/
│   │   ├── test_api.py
│   │   └── test_day4_project_ownership.py
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

The original `Project` table included:

* `id`

* `title`

* `description`

* `created_at`

* `updated_at`

* Added Pydantic schemas in:

```txt
backend/app/schemas.py
```

Initial schemas:

* `ProjectBase`

* `ProjectCreate`

* `ProjectUpdate`

* `ProjectRead`

* Added project routes in:

```txt
backend/app/routers/projects.py
```

Initial project API routes:

```txt
POST   /projects
GET    /projects
GET    /projects/{project_id}
PATCH  /projects/{project_id}
DELETE /projects/{project_id}
```

At the end of Day 2, project routes were public and not yet connected to users.

---

## What I Built on Day 3

Day 3 focused on authentication basics.

Completed:

* Added `User` SQLAlchemy model.

* Created `users` table in PostgreSQL.

* Added Pydantic schemas:

  * `UserCreate`
  * `UserLogin`
  * `UserRead`
  * `Token`

* Added password hashing with `pwdlib[argon2]`.

* Added JWT creation and decoding with `PyJWT`.

* Added JWT config:

  * `SECRET_KEY`
  * `ALGORITHM=HS256`
  * `ACCESS_TOKEN_EXPIRE_MINUTES=30`

* Added auth routes:

  * `POST /auth/register`
  * `POST /auth/login`
  * `GET /auth/me`

* Added reusable auth dependency:

  * `get_current_user`

* Added automated tests for:

  * user registration
  * duplicate email handling
  * hashed password storage
  * login success
  * login failure
  * JWT token response
  * `/auth/me` with a valid token
  * `/auth/me` without a token

### Auth Flow

1. User registers with email and password.
2. Backend hashes the password before saving it.
3. User logs in with email and password.
4. Backend verifies the password against the stored hash.
5. Backend returns a JWT access token.
6. Protected routes use the bearer token to identify the current user.

### Auth Endpoints

| Method | Endpoint         | Description                       |
| ------ | ---------------- | --------------------------------- |
| `POST` | `/auth/register` | Create a new user                 |
| `POST` | `/auth/login`    | Log in and receive a JWT          |
| `GET`  | `/auth/me`       | Return the current logged-in user |

---

## What I Built on Day 4

Day 4 focused on connecting projects to users and protecting project routes.

Completed:

* Added `owner_id` to the `Project` model.

* Added a foreign key from `projects.owner_id` to `users.id`.

* Added SQLAlchemy relationships:

  * `User.projects`
  * `Project.owner`

* Updated project creation so new projects belong to the logged-in user.

* Protected all project routes with JWT authentication.

* Updated `GET /projects` so users only see their own projects.

* Updated `GET /projects/{project_id}` so only the owner can access a project.

* Updated `PATCH /projects/{project_id}` so only the owner can update a project.

* Updated `DELETE /projects/{project_id}` so only the owner can delete a project.

* Added helper logic to fetch only projects owned by the current user.

* Added tests for authenticated project CRUD.

* Added tests for private project lists.

* Added tests for owner-only access.

* Added tests for SQLAlchemy user-project relationships.

* Verified the real Postgres schema with `psql`.

### Current User-Owned Project Flow

1. User registers with email/password.
2. Password is hashed before storage.
3. User logs in and receives a JWT access token.
4. Client sends the JWT as a bearer token.
5. Protected routes use `get_current_user`.
6. New projects are saved with:

```txt
owner_id = current_user.id
```

7. Project queries filter by:

```txt
Project.owner_id == current_user.id
```

This means users can only see, update, and delete their own projects.

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

## Auth API

### Register User

```txt
POST /auth/register
```

Example request:

```json
{
  "email": "joe@example.com",
  "password": "password123"
}
```

Example response:

```json
{
  "id": 1,
  "email": "joe@example.com",
  "created_at": "2026-06-13T17:00:00Z",
  "updated_at": "2026-06-13T17:00:00Z"
}
```

The API never returns the raw password or password hash.

---

### Login User

```txt
POST /auth/login
```

Example request:

```json
{
  "email": "joe@example.com",
  "password": "password123"
}
```

Example response:

```json
{
  "access_token": "jwt_token_here",
  "token_type": "bearer"
}
```

---

### Get Current User

```txt
GET /auth/me
```

Requires:

```txt
Authorization: Bearer <access_token>
```

Example response:

```json
{
  "id": 1,
  "email": "joe@example.com",
  "created_at": "2026-06-13T17:00:00Z",
  "updated_at": "2026-06-13T17:00:00Z"
}
```

---

## Project API

All project routes now require authentication.

Each request must include:

```txt
Authorization: Bearer <access_token>
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
  "owner_id": 1,
  "created_at": "2026-06-13T17:00:00Z",
  "updated_at": "2026-06-13T17:00:00Z"
}
```

The request body does not include `owner_id`.

The backend gets `owner_id` from the logged-in user.

---

### List Projects

```txt
GET /projects
```

Returns only projects owned by the current logged-in user.

Example response:

```json
[
  {
    "title": "First Research Project",
    "description": "Testing project creation through the API",
    "id": 1,
    "owner_id": 1,
    "created_at": "2026-06-13T17:00:00Z",
    "updated_at": "2026-06-13T17:00:00Z"
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

If the project exists and belongs to the current user, it returns that project.

If it does not exist or belongs to another user, it returns:

```json
{
  "detail": "Project not found"
}
```

The API intentionally returns `404` for another user's project so it does not reveal whether private data exists.

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

Only the project owner can update the project.

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

Only the project owner can delete the project.

---

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
SECRET_KEY=change_me_to_a_long_random_secret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
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
PYTHONPATH=backend .venv/bin/uvicorn app.main:app --reload
```

Why `PYTHONPATH=backend` is needed:

The backend code imports modules like:

```python
from app.database import Base
```

So Python needs to know that `backend/` is the folder where the `app` package lives.

---

## Running Tests

Run all backend tests from the project root:

```bash
PYTHONPATH=backend .venv/bin/pytest backend/tests -q
```

The tests use a temporary SQLite database so they do not require the local Postgres container.

Current test coverage includes:

* health route
* project CRUD
* user registration
* duplicate email failure
* hashed password storage
* login success
* login failure
* JWT token response
* `/auth/me`
* protected project routes
* user-owned project creation
* private project lists
* owner-only get/update/delete behavior
* SQLAlchemy user-project relationships

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

## Current Database Schema

### users

```txt
id
email
hashed_password
created_at
updated_at
```

Important constraints:

* `id` is the primary key.
* `email` is unique.
* `hashed_password` stores the Argon2 password hash.

### projects

```txt
id
title
description
owner_id
created_at
updated_at
```

Important constraints:

* `id` is the primary key.
* `owner_id` is required.
* `owner_id` is a foreign key to `users.id`.

Relationship:

```txt
users.id  ->  projects.owner_id
```

Meaning:

```txt
One user can own many projects.
Each project belongs to one user.
```

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

Describe the users table:

```sql
\d users
```

Check project ownership with a join:

```sql
SELECT
  projects.id,
  projects.title,
  projects.owner_id,
  users.email
FROM projects
JOIN users ON projects.owner_id = users.id;
```

Exit `psql`:

```sql
\q
```

---

## Example Curl Commands

### Register

```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"email":"joe@example.com","password":"password123"}'
```

### Login

```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"joe@example.com","password":"password123"}'
```

Copy the `access_token` from the login response.

Set it as a shell variable:

```bash
TOKEN="paste_access_token_here"
```

### Get Current User

```bash
curl "http://localhost:8000/auth/me" \
  -H "Authorization: Bearer $TOKEN"
```

### Create a Project

```bash
curl -X POST "http://localhost:8000/projects" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"title":"My project","description":"notes"}'
```

### List Current User's Projects

```bash
curl "http://localhost:8000/projects" \
  -H "Authorization: Bearer $TOKEN"
```

### Get One Project

```bash
curl "http://localhost:8000/projects/1" \
  -H "Authorization: Bearer $TOKEN"
```

### Update a Project

```bash
curl -X PATCH "http://localhost:8000/projects/1" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"title":"Updated title"}'
```

### Delete a Project

```bash
curl -X DELETE "http://localhost:8000/projects/1" \
  -H "Authorization: Bearer $TOKEN"
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

For auth routes, make sure `auth` is also included:

```python
from app.routers import auth

app.include_router(auth.router)
```

### `column projects.owner_id does not exist`

This means the Python model has changed, but the existing Postgres table has not.

Because Alembic migrations are not implemented yet, reset the dev database:

```bash
docker compose down -v
docker compose up -d postgres
```

Then restart the backend so tables are recreated.

Warning: this deletes local database data.

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
* How SQLAlchemy relationships connect models.
* How foreign keys connect database tables.
* How Pydantic validates API input and output.
* How environment variables configure apps.
* How local development differs from containerized development.
* How password hashing works.
* How JWT-based authentication works.
* How bearer tokens protect API routes.
* How authenticated routes use the current user.
* How authorization differs from authentication.
* How to write backend tests with pytest and TestClient.
* How to build CRUD routes step by step.

---

## Next Steps

Day 5 will add database migrations.

Planned Day 5 work:

* Add Alembic.
* Initialize migrations.
* Create the first migration for the current schema.
* Learn why `create_all()` is not enough for real projects.
* Learn how to upgrade and downgrade database schema versions.
* Remove the need to reset the Postgres volume for every model change.

Later milestones:

* React + TypeScript frontend.
* Document upload/notes system.
* Chunking and embeddings.
* RAG search over project documents.
* AI-generated research memos.
* GitHub Actions CI.
* Deployment.
* Kubernetes and Terraform basics.
