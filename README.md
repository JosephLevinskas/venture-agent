# VentureAgent

VentureAgent is a full-stack AI research workspace for creating research projects, saving notes/documents, and preparing for future retrieval-augmented generation features like embeddings, vector search, evidence-based Q&A, and structured research report generation.

## Current Features

* React + TypeScript frontend built with Vite.
* FastAPI backend with PostgreSQL persistence.
* User registration and login.
* Password hashing with Argon2.
* JWT-based authentication.
* Protected project CRUD routes.
* User-owned projects with ownership checks.
* Documents/notes attached to projects.
* Protected document CRUD routes.
* Database migrations with Alembic.
* Docker Compose PostgreSQL setup.
* Backend test suite with pytest and FastAPI TestClient.

## Tech Stack

### Frontend

* React
* TypeScript
* Vite
* CSS

### Backend

* Python 3.12
* FastAPI
* Uvicorn
* SQLAlchemy
* Alembic
* Pydantic
* PyJWT
* pwdlib[argon2]
* python-dotenv

### Database / DevOps

* PostgreSQL 16
* Docker
* Docker Compose

### Testing

* pytest
* FastAPI TestClient
* Temporary SQLite test database

## Architecture

Current data model:

```txt
User -> Project -> Document
```

* A user can own many projects.
* A project belongs to one user.
* A project can have many documents.
* A document belongs to one project.
* Document access is protected through the parent project owner.

Important ownership rules:

* The frontend never sends `owner_id`.
* The backend gets the current user from the JWT.
* Project queries filter by `Project.owner_id == current_user.id`.
* Document access checks the owner through `Document -> Project -> User`.

## API Overview

### Auth

```txt
POST /auth/register
POST /auth/login
GET  /auth/me
```

### Projects

```txt
POST   /projects
GET    /projects
GET    /projects/{project_id}
PATCH  /projects/{project_id}
DELETE /projects/{project_id}
```

### Documents

```txt
POST   /projects/{project_id}/documents
GET    /projects/{project_id}/documents
GET    /documents/{document_id}
PATCH  /documents/{document_id}
DELETE /documents/{document_id}
```

## Project Structure

```txt
venture-agent/
├── backend/
│   ├── alembic/
│   ├── app/
│   │   ├── main.py
│   │   ├── database.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── security.py
│   │   ├── dependencies.py
│   │   └── routers/
│   │       ├── auth.py
│   │       ├── projects.py
│   │       └── documents.py
│   ├── tests/
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.tsx
│   │   ├── App.css
│   │   ├── index.css
│   │   └── main.tsx
│   ├── package.json
│   └── vite.config.ts
├── docker-compose.yml
├── alembic.ini
├── .env.example
└── README.md
```

## Local Setup

### 1. Backend environment

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
```

### 2. Environment variables

Create `.env` from `.env.example`.

Example local values:

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=venture_agent
DATABASE_URL=postgresql://postgres:postgres@127.0.0.1:5433/venture_agent
SECRET_KEY=change_me_to_a_long_random_secret_at_least_32_bytes
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 3. Start Postgres

```bash
docker compose up -d postgres
```

### 4. Run migrations

```bash
.venv/bin/alembic upgrade head
```

### 5. Run backend

```bash
PYTHONPATH=backend .venv/bin/uvicorn app.main:app --reload
```

Backend:

```txt
http://localhost:8000
```

API docs:

```txt
http://localhost:8000/docs
```

### 6. Run frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend:

```txt
http://localhost:5173
```

## Testing

Run backend tests:

```bash
PYTHONPATH=backend .venv/bin/pytest backend/tests -q
```

Current test coverage includes:

* Health route.
* User registration/login.
* JWT authentication.
* Password hashing.
* Protected project routes.
* User-owned project access control.
* Protected document routes.
* Document ownership through parent project.
* Cascade delete from projects to documents.

## Database Migrations

Alembic owns schema changes.

Create a migration:

```bash
.venv/bin/alembic revision --autogenerate -m "message"
```

Apply migrations:

```bash
.venv/bin/alembic upgrade head
```

Check current migration:

```bash
.venv/bin/alembic current
```

Current migrations:

```txt
create users and projects
add documents
```

## Useful Commands

Start database:

```bash
docker compose up -d postgres
```

Stop services:

```bash
docker compose down
```

Delete local database volume:

```bash
docker compose down -v
```

Open Postgres shell:

```bash
docker compose exec postgres psql -U postgres -d venture_agent
```

Inspect tables:

```sql
\dt
\d users
\d projects
\d documents
SELECT * FROM alembic_version;
```

Run all tests:

```bash
PYTHONPATH=backend .venv/bin/pytest backend/tests -q
```

## Resume Bullets

* Built a full-stack research workspace using React, TypeScript, FastAPI, PostgreSQL, SQLAlchemy, and Docker.
* Implemented JWT authentication with Argon2 password hashing and protected user-specific API routes.
* Designed relational data models for users, projects, and documents with ownership-based access control.
* Added Alembic migrations to manage PostgreSQL schema changes across development.
* Built a React frontend for login, project creation, project selection, document creation, and document viewing.
* Wrote backend tests covering authentication, protected CRUD routes, ownership checks, and document access control.

## Next Steps

* Add document chunking.
* Add embeddings and vector storage.
* Add RAG Q&A with cited evidence.
* Add structured research memo generation.
* Add GitHub Actions CI.
* Add deployment configuration.
