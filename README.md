# VentureAgent

`VentureAgent` is a full-stack AI research agent project. The goal is to build a backend-first application that can manage research projects, store documents/notes, and later use retrieval, embeddings, vector search, and LLMs to generate structured research reports.

This repo is being built as a 14-day project sprint to learn backend engineering, databases, Docker, authentication, migrations, testing, full-stack development, CI, and deployment patterns.

---

## Current Status

The backend is complete through the current Day 5 milestone.

Completed so far:

* Day 1: project setup, FastAPI backend, Docker, Docker Compose, PostgreSQL.
* Day 2: project CRUD with SQLAlchemy and Pydantic.
* Day 3: authentication basics with users, password hashing, login, JWTs, and `/auth/me`.
* Day 4 backend ownership work: user-owned projects and protected project routes.
* Day 5 backend work: Alembic migrations and documents/notes attached to projects.

Important note:

* The original sprint planned React + TypeScript frontend basics for Day 4.
* The backend is ahead in some areas because Alembic and documents are now implemented.
* The frontend is still pending and should be the next catch-up milestone.

The project currently has:

* A FastAPI backend.
* PostgreSQL running through Docker Compose.
* SQLAlchemy models.
* Alembic database migrations.
* A working `User` model.
* A working `Project` model.
* A working `Document` model.
* User registration and login.
* Password hashing with Argon2.
* JWT access token creation and decoding.
* A reusable `get_current_user` dependency.
* Protected project CRUD routes.
* User-owned projects.
* Protected document/note routes.
* Documents attached to projects.
* Ownership checks so users cannot access another user's projects or documents.
* Automated backend tests with `pytest` and FastAPI `TestClient`.
* Swagger/OpenAPI docs available at `/docs`.

No frontend has been implemented yet.

---

## Tech Stack

### Backend

* Python 3.12
* FastAPI
* Uvicorn
* SQLAlchemy
* Alembic
* Pydantic
* psycopg2-binary
* python-dotenv
* pwdlib[argon2]
* PyJWT

### Database

* PostgreSQL 16
* Docker volume for persistent database storage
* Alembic for schema migrations

### Testing

* pytest
* FastAPI TestClient
* Temporary SQLite test database

### DevOps / Tooling

* Docker
* Docker Compose
* Git / GitHub

### Planned Later

* React + TypeScript frontend
* Document upload support
* Chunking
* Embeddings / vector search
* RAG question answering
* Structured research memo generation
* Agent-style workflow
* GitHub Actions CI
* Deployment
* Kubernetes / Terraform basics

---

## Project Structure

```txt
venture-agent/
├── backend/
│   ├── alembic/
│   │   ├── env.py
│   │   ├── script.py.mako
│   │   └── versions/
│   │       ├── b7f820c358cc_create_users_and_projects.py
│   │       └── 707473e937cc_add_documents.py
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
│   │       ├── projects.py
│   │       └── documents.py
│   ├── tests/
│   │   ├── test_api.py
│   │   ├── test_day4_project_ownership.py
│   │   └── test_day5_documents.py
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
├── infra/
├── docs/
├── alembic.ini
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

* Verified the backend could run locally and through Docker.

The health endpoint:

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

The first real domain object was `Project`.

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

* Created `users` table.

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

## What I Built on Day 5

Day 5 focused on database migrations and documents/notes attached to projects.

Completed:

* Added Alembic.
* Initialized Alembic in:

```txt
backend/alembic/
```

* Configured Alembic to read the app's SQLAlchemy metadata.
* Configured Alembic to read `DATABASE_URL` from `.env`.
* Commented out `Base.metadata.create_all(bind=engine)` in `main.py`.
* Created the initial migration:

```txt
create users and projects
```

* Applied the initial migration with:

```bash
.venv/bin/alembic upgrade head
```

* Verified the `alembic_version` table in Postgres.

* Added a `Document` SQLAlchemy model.

* Added a foreign key from `documents.project_id` to `projects.id`.

* Added SQLAlchemy relationships:

  * `Project.documents`
  * `Document.project`

* Added document schemas:

  * `DocumentBase`
  * `DocumentCreate`
  * `DocumentRead`
  * `DocumentUpdate`

* Added document routes:

```txt
POST   /projects/{project_id}/documents
GET    /projects/{project_id}/documents
GET    /documents/{document_id}
PATCH  /documents/{document_id}
DELETE /documents/{document_id}
```

* Created and applied the Alembic migration:

```txt
add documents
```

* Verified the `documents` table in Postgres.
* Added tests for:

  * document routes requiring authentication
  * creating documents on owned projects
  * preventing document creation on another user's project
  * listing documents only for owned projects
  * getting documents only as the project owner
  * updating documents only as the project owner
  * deleting documents only as the project owner
  * deleting attached documents when a project is deleted

### Current Document Ownership Flow

Documents do not store their own `owner_id`.

Instead, ownership is inherited through the project:

```txt
User -> Project -> Document
```

The API checks document access by following:

```txt
document.project.owner_id == current_user.id
```

This means users can only access documents attached to projects they own.

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

All project routes require authentication.

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

---

### Get One Project

```txt
GET /projects/{project_id}
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

This route supports partial updates.

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

Deleting a project also deletes attached documents.

---

## Document API

All document routes require authentication.

Documents are scoped through their parent project.

Each request must include:

```txt
Authorization: Bearer <access_token>
```

---

### Create Document

```txt
POST /projects/{project_id}/documents
```

Example request:

```json
{
  "title": "Research Note 1",
  "content": "These are my notes for this project."
}
```

Example response:

```json
{
  "id": 1,
  "project_id": 1,
  "title": "Research Note 1",
  "content": "These are my notes for this project.",
  "created_at": "2026-06-13T17:00:00Z",
  "updated_at": "2026-06-13T17:00:00Z"
}
```

Only the project owner can create documents for that project.

---

### List Documents for a Project

```txt
GET /projects/{project_id}/documents
```

Returns only documents for a project owned by the current user.

If the project belongs to another user, the API returns:

```json
{
  "detail": "Project not found"
}
```

---

### Get One Document

```txt
GET /documents/{document_id}
```

If the document exists and belongs to a project owned by the current user, it returns the document.

If the document does not exist or belongs to another user's project, it returns:

```json
{
  "detail": "Document not found"
}
```

---

### Update Document

```txt
PATCH /documents/{document_id}
```

Example request:

```json
{
  "title": "Updated Research Note"
}
```

This route supports partial updates.

Only the owner of the parent project can update the document.

---

### Delete Document

```txt
DELETE /documents/{document_id}
```

Example response:

```json
{
  "message": "Document deleted successfully"
}
```

Only the owner of the parent project can delete the document.

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
SECRET_KEY=change_me_to_a_long_random_secret_at_least_32_bytes
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Do not commit `.env`.

---

## Running with Docker Compose

Start Postgres:

```bash
docker compose up -d postgres
```

Apply database migrations:

```bash
.venv/bin/alembic upgrade head
```

Run the backend locally:

```bash
PYTHONPATH=backend .venv/bin/uvicorn app.main:app --reload
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

## Running Backend and Postgres Fully Through Docker Compose

Start all services:

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

Note:

Because migrations are now handled by Alembic, the database should be migrated with:

```bash
.venv/bin/alembic upgrade head
```

before relying on the app against a fresh database.

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
* protected document routes
* document creation on owned projects
* blocked document creation on another user's project
* private document lists
* owner-only document get/update/delete behavior
* cascade delete from project to documents

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

Important idea:

```txt
Mac Python uses:        127.0.0.1:5433
Docker backend uses:    postgres:5432
```

Both point to the same Postgres database, but from different network locations.

---

## Alembic Migration Workflow

Alembic now owns database schema changes.

The app no longer uses:

```python
Base.metadata.create_all(bind=engine)
```

Normal migration workflow:

```bash
.venv/bin/alembic revision --autogenerate -m "describe schema change"
.venv/bin/alembic upgrade head
```

Check current database migration version:

```bash
.venv/bin/alembic current
```

View migration history:

```bash
.venv/bin/alembic history
```

Downgrade one migration:

```bash
.venv/bin/alembic downgrade -1
```

Current migrations:

```txt
b7f820c358cc_create_users_and_projects.py
707473e937cc_add_documents.py
```

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

---

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
users.id -> projects.owner_id
```

Meaning:

```txt
One user can own many projects.
Each project belongs to one user.
```

---

### documents

```txt
id
project_id
title
content
created_at
updated_at
```

Important constraints:

* `id` is the primary key.
* `project_id` is required.
* `project_id` is a foreign key to `projects.id`.

Relationship:

```txt
projects.id -> documents.project_id
```

Meaning:

```txt
One project can have many documents.
Each document belongs to one project.
```

---

## Useful Commands

Start Postgres:

```bash
docker compose up -d postgres
```

Start all services:

```bash
docker compose up -d --build
```

Apply migrations:

```bash
.venv/bin/alembic upgrade head
```

Check current migration:

```bash
.venv/bin/alembic current
```

Create a new migration:

```bash
.venv/bin/alembic revision --autogenerate -m "message"
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

Describe tables:

```sql
\d users
\d projects
\d documents
```

Check Alembic version:

```sql
SELECT * FROM alembic_version;
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

Check document ownership through projects:

```sql
SELECT
  documents.id,
  documents.title,
  documents.project_id,
  projects.title AS project_title,
  users.email AS owner_email
FROM documents
JOIN projects ON documents.project_id = projects.id
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

### Create a Document

```bash
curl -X POST "http://localhost:8000/projects/1/documents" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"title":"Research Note","content":"These are my notes."}'
```

### List Documents for a Project

```bash
curl "http://localhost:8000/projects/1/documents" \
  -H "Authorization: Bearer $TOKEN"
```

### Get One Document

```bash
curl "http://localhost:8000/documents/1" \
  -H "Authorization: Bearer $TOKEN"
```

### Update a Document

```bash
curl -X PATCH "http://localhost:8000/documents/1" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"title":"Updated Note Title"}'
```

### Delete a Document

```bash
curl -X DELETE "http://localhost:8000/documents/1" \
  -H "Authorization: Bearer $TOKEN"
```

---

## Troubleshooting

### `password authentication failed for user "postgres"`

This usually means the Postgres volume was initialized with old credentials.

If it is okay to delete local database data, reset with:

```bash
docker compose down -v
docker compose up -d postgres
.venv/bin/alembic upgrade head
```

### `DATABASE_URL is not set`

The backend and Alembic need `DATABASE_URL`.

Make sure `.env` includes:

```env
DATABASE_URL=postgresql://postgres:postgres@127.0.0.1:5433/venture_agent
```

For Docker backend service networking, the backend container may need:

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

Then start Postgres:

```bash
docker compose up -d postgres
```

### Route exists in file but not in `/docs`

Make sure the router is included in `main.py`:

```python
from app.routers import auth, projects, documents

app.include_router(auth.router)
app.include_router(projects.router)
app.include_router(documents.router)
```

### `column projects.owner_id does not exist`

This means the database has not been migrated.

Run:

```bash
.venv/bin/alembic upgrade head
```

### `relation "documents" does not exist`

This means the documents migration has not been applied.

Run:

```bash
.venv/bin/alembic upgrade head
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
* How database migrations work.
* Why `create_all()` is not enough for real projects.
* How Alembic tracks schema versions.
* How to write backend tests with pytest and TestClient.
* How to protect nested resources like documents through parent ownership.
* How to build CRUD routes step by step.

---

## Next Steps

Immediate next milestone:

* Add the React + TypeScript frontend MVP that was originally planned for Day 4.

Frontend MVP should support:

* Register.
* Login.
* Store JWT token.
* Create projects.
* List current user's projects.
* Create notes/documents under a selected project.
* List documents for a selected project.

Upcoming backend milestones:

* Chunking documents.
* Embeddings.
* Vector storage.
* RAG Q&A with evidence.
* Structured research memo generator.
* Agent-style workflow.
* GitHub Actions CI.
* Docker polish and deployment.
* Security scanning/docs/audit logs.
* Kubernetes and Terraform basics.
