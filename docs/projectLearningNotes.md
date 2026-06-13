# VentureAgent Notes — Days 1–3

## Project Overview

VentureAgent is a full-stack AI research agent project.

Long-term goal:

Users will be able to create research projects, attach documents/notes, search through their material with embeddings/vector search/RAG, and generate structured research reports.

Current stack:

* FastAPI backend
* Uvicorn server
* PostgreSQL database
* SQLAlchemy ORM
* psycopg2-binary Postgres driver
* Pydantic schemas
* python-dotenv for `.env`
* Docker + Docker Compose
* JWT authentication
* Password hashing with `pwdlib[argon2]`
* PyJWT for token creation/verification
* React/TypeScript frontend later
* RAG/vector search/LLM reports later
* GitHub Actions/CI later
* Deployment later

---

# Day 1 — Project Setup, FastAPI, Docker, Postgres, GitHub

## Goal

Set up the project foundation:

* project folders
* Git repo
* FastAPI backend
* health check route
* Docker backend container
* Docker Compose
* PostgreSQL service
* `.env` config
* GitHub push

---

## Command Line Basics

`pwd`

Print working directory.

Shows the full path of the folder you are currently in.

Example:

```bash
pwd
```

---

`cd`

Change directory.

Examples:

```bash
cd backend
```

Move into the `backend` folder.

```bash
cd ..
```

Move up one parent folder.

```bash
cd .
```

Stay in the current folder.

---

`mkdir`

Make a new directory.

Example:

```bash
mkdir backend frontend infra docs
```

Creates those folders.

---

`ls`

List files/folders in the current directory.

```bash
ls
```

---

`ls -a`

List all files, including hidden files like `.git`, `.env`, `.venv`.

```bash
ls -a
```

---

`touch`

Create empty files.

Example:

```bash
touch README.md .gitignore .env.example docker-compose.yml
```

---

`cat`

Print the contents of a file into the terminal.

Example:

```bash
cat README.md
```

---

## Project Root

The project root is the main folder for the whole repo.

For this project:

```txt
venture-agent/
```

Everything lives inside it.

---

## Main Folders

```txt
venture-agent/
  backend/
  frontend/
  infra/
  docs/
```

`backend/`

FastAPI server code.

`frontend/`

React/TypeScript app later.

`infra/`

Docker, deployment, cloud, Kubernetes, Terraform later.

`docs/`

Architecture notes, security notes, research notes, design writeups later.

Why this matters:

A clean folder structure makes the project easier to understand, maintain, expand, debug, and show to employers.

---

## Git Basics

Git is version control software.

It tracks changes to a project over time.

A repository, or repo, is a folder that Git is tracking.

---

`git init`

Start tracking the current folder with Git.

```bash
git init
```

---

`git status`

Show the current state of the repo.

It tells you:

* what branch you are on
* what files changed
* what files are untracked
* what is staged
* whether there is anything to commit

```bash
git status
```

---

`git add .`

Stage all current changes in the current folder.

Staging means choosing what goes into the next commit.

```bash
git add .
```

---

`git commit -m "message"`

Create a saved checkpoint.

```bash
git commit -m "Initial project setup"
```

A commit is a saved checkpoint in the project history.

---

`working tree clean`

Means all tracked changes are committed and there is nothing new to commit.

---

## GitHub Remote

A remote is a named link from your local Git repo to an online repo.

Usually the remote is named `origin`.

`origin` is just a nickname for the GitHub repo URL.

---

`git remote add origin <url>`

Connect local repo to GitHub.

```bash
git remote add origin https://github.com/JosephLevinskas/venture-agent.git
```

---

`git push -u origin main`

Push local commits to GitHub.

```bash
git push -u origin main
```

Meaning:

* `git push` = send commits to remote
* `-u` = remember this branch/remote connection
* `origin` = remote nickname
* `main` = branch being pushed

After this, future pushes can usually just be:

```bash
git push
```

---

## Starter Files

`README.md`

Explains what the project is and how to run it.

Important because people may not read all the code.

---

`.gitignore`

Tells Git which files/folders not to track.

Important ignored files:

```txt
.venv/
.env
__pycache__/
*.pyc
.DS_Store
```

`.venv/`

Local Python environment. Do not commit.

`.env`

Real local secrets/config. Do not commit.

`__pycache__/` and `*.pyc`

Python-generated cache files. Do not commit.

`.DS_Store`

macOS metadata junk. Do not commit.

---

`.env.example`

Safe template showing what environment variables the project needs.

Commit this.

Example:

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=venture_agent
POSTGRES_PORT=5432
DATABASE_URL=postgresql://postgres:postgres@127.0.0.1:5433/venture_agent
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

`.env`

Real local values.

Do not commit this.

Example local values:

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=venture_agent
POSTGRES_PORT=5432
DATABASE_URL=postgresql://postgres:postgres@127.0.0.1:5433/venture_agent
SECRET_KEY=dev_secret_key_32_bytes_minimum_change_later
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

## Python Virtual Environment

`.venv`

A local isolated Python environment.

Why it matters:

It keeps this project’s Python packages separate from other projects.

Activate it:

```bash
source .venv/bin/activate
```

Install packages:

```bash
pip install -r backend/requirements.txt
```

Commit `requirements.txt`.

Do not commit `.venv/`.

---

## Backend Skeleton

Minimum backend setup:

```txt
backend/
  app/
    main.py
  tests/
  requirements.txt
  Dockerfile
```

`backend/app/`

Actual backend application code.

`backend/tests/`

Backend tests.

`backend/requirements.txt`

Python dependency list.

`backend/Dockerfile`

Instructions for Docker to package/run the backend.

---

## FastAPI

FastAPI is a Python framework for building backend APIs.

An API is how the frontend, browser, or another program talks to your backend.

---

## Uvicorn

Uvicorn is the server that runs the FastAPI app.

FastAPI defines the app.

Uvicorn serves it over HTTP.

---

## Route

A route is a URL path that triggers backend code.

Example:

```python
@app.get("/health")
def health_check():
    return {"status": "ok"}
```

When the backend receives:

```txt
GET /health
```

it runs:

```python
health_check()
```

---

## JSON

JSON is a common API data format.

Example:

```json
{
  "status": "ok"
}
```

Frontend and backend usually communicate with JSON.

---

## Decorator

A Python decorator starts with `@`.

FastAPI uses decorators to connect routes to functions.

Example:

```python
@app.get("/health")
def health_check():
    return {"status": "ok"}
```

`@app.get("/health")` attaches the route to the function below it.

---

## FastAPI App Object

The FastAPI app object is the main backend application.

Example:

```python
from fastapi import FastAPI

app = FastAPI(title="VentureAgent API")
```

It stores routes and app configuration.

---

## Running Locally

Install dependencies:

```bash
python3 -m pip install -r backend/requirements.txt
```

Run locally from project root:

```bash
uvicorn backend.app.main:app --reload
```

Meaning:

* `uvicorn` = server
* `backend.app.main` = Python import path to `main.py`
* `:app` = FastAPI app object inside that file
* `--reload` = restart automatically when code changes

Open:

```txt
http://localhost:8000/health
```

Expected:

```json
{
  "status": "ok"
}
```

Open docs:

```txt
http://localhost:8000/docs
```

FastAPI automatically generates API docs.

---

## Dockerfile

A Dockerfile is a recipe for building a Docker image.

A Docker image is a packaged version of your app environment.

A container is a running image.

---

## Dockerfile Instructions

`FROM`

Choose the base environment.

Example:

```dockerfile
FROM python:3.12-slim
```

---

`WORKDIR`

Set the folder inside the container where commands run.

Example:

```dockerfile
WORKDIR /app
```

---

`COPY`

Copy files from your computer into the image.

Example:

```dockerfile
COPY requirements.txt .
COPY . .
```

---

`RUN`

Run a command while building the image.

Example:

```dockerfile
RUN pip install -r requirements.txt
```

---

`CMD`

Command that runs when the container starts.

Example:

```dockerfile
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

`--host 0.0.0.0`

Makes the FastAPI server reachable from outside the container.

Inside Docker, this matters because `127.0.0.1` would only listen inside the container.

---

## Build Backend Docker Image

```bash
docker build -t venture-agent-backend ./backend
```

Meaning:

* `docker build` = create an image from a Dockerfile
* `-t venture-agent-backend` = name the image
* `./backend` = build context

Docker build context means the folder Docker can see while building.

---

## Docker Daemon

The Docker daemon is the Docker engine.

It must be running before Docker commands work.

---

## Run Backend Container

```bash
docker run --rm -p 8000:8000 venture-agent-backend
```

Meaning:

* `docker run` = start a container from an image
* `--rm` = delete the container after it stops
* `-p 8000:8000` = map Mac port 8000 to container port 8000
* `venture-agent-backend` = image name

Open:

```txt
http://localhost:8000/health
```

---

## Docker Compose

Docker Compose runs multiple containers together.

Instead of manually running backend and Postgres separately, `docker-compose.yml` describes the whole stack.

Run:

```bash
docker compose up --build
```

Meaning:

* build images if needed
* start services together

---

## Docker Compose Service

A service is one running part of the app.

Current services:

```txt
backend
postgres
```

---

## PostgreSQL / Postgres

PostgreSQL, usually called Postgres, is the database.

The app needs a database to store users, projects, documents, etc.

We use the official Docker image:

```txt
postgres:16
```

---

## Postgres Volume

Containers can be deleted/recreated, but database data should persist.

A volume stores database data outside the container.

Example:

```yaml
volumes:
  postgres_data:
```

Service usage:

```yaml
- postgres_data:/var/lib/postgresql/data
```

This stores Postgres data in a named Docker volume.

---

## `depends_on`

`depends_on` tells Docker Compose to start one service before another.

Example:

```yaml
depends_on:
  - postgres
```

This starts Postgres before the backend.

Important:

`depends_on` controls startup order, but it does not guarantee Postgres is fully ready to accept connections.

---

## `.env` Variable Substitution in Compose

Docker Compose can read values from `.env`.

Example:

```yaml
POSTGRES_USER: ${POSTGRES_USER}
```

`${POSTGRES_USER}` means:

Use the value from `.env`.

Important:

If a Postgres volume already exists, changing `.env` later does not automatically recreate the database user/database. The old data remains in the volume.

---

## Local vs Docker Database URLs

Local Mac Python connects through the mapped host port:

```env
DATABASE_URL=postgresql://postgres:postgres@127.0.0.1:5433/venture_agent
```

Backend container connects through the Docker service name:

```env
DATABASE_URL=postgresql://postgres:postgres@postgres:5432/venture_agent
```

Why:

Inside Docker, `127.0.0.1` means “inside this same container.”

The backend container needs to reach the Postgres container by service name:

```txt
postgres
```

---

## Day 1 Summary

Completed:

* Created project root
* Created `backend/`, `frontend/`, `infra/`, `docs/`
* Initialized Git
* Added `.gitignore`
* Added `.env.example`
* Added `README.md`
* Added `docker-compose.yml`
* Created FastAPI backend
* Added `/health`
* Created `.venv`
* Installed FastAPI and Uvicorn
* Ran backend locally
* Created Dockerfile
* Built backend Docker image
* Ran backend container
* Added Docker Compose backend service
* Added Postgres service
* Added Postgres volume
* Added `depends_on`
* Used `.env` values in Compose
* Pushed repo to GitHub

Core result:

FastAPI + Docker + Compose + Postgres + GitHub all working.

---

# Day 2 — Projects CRUD with SQLAlchemy and Postgres

## Goal

Make the app store and manage project data.

CRUD means:

* Create
* Read
* Update
* Delete

Endpoints built:

```txt
POST /projects
GET /projects
GET /projects/{project_id}
PATCH /projects/{project_id}
DELETE /projects/{project_id}
```

---

## Branch Workflow

Created a feature branch:

```bash
git checkout -b feature/projects-crud
```

Why:

`main` stays stable.

`feature/projects-crud` is where new work happens.

After work is complete and tested, merge back into `main`.

---

## Database Dependencies

Installed:

```txt
sqlalchemy
psycopg2-binary
python-dotenv
```

---

## SQLAlchemy

SQLAlchemy lets Python code interact with the database.

Instead of writing raw SQL for everything, we can define Python models and use Python methods.

SQLAlchemy organizes the database work.

---

## psycopg2-binary

`psycopg2-binary` is the Postgres driver.

SQLAlchemy organizes the work.

`psycopg2-binary` physically lets Python talk to Postgres.

---

## python-dotenv

`python-dotenv` lets Python read `.env` values.

Used so config/secrets stay outside the code.

---

## Database URL

A database URL is one string that tells the backend how to find the database.

Format:

```txt
postgresql://USER:PASSWORD@HOST:PORT/DATABASE_NAME
```

Example local Mac URL:

```txt
postgresql://postgres:postgres@127.0.0.1:5433/venture_agent
```

Example Docker backend URL:

```txt
postgresql://postgres:postgres@postgres:5432/venture_agent
```

---

## `database.py`

Purpose:

`database.py` is the connection layer between FastAPI and the database.

It defines:

* `DATABASE_URL`
* `engine`
* `SessionLocal`
* `Base`
* `get_db()`

---

## `os`

`os` is a built-in Python module.

Used to read environment variables.

Example:

```python
os.getenv("DATABASE_URL")
```

---

## `load_dotenv()`

Loads variables from `.env` into the Python environment.

Example:

```python
from dotenv import load_dotenv

load_dotenv()
```

---

## `create_engine()`

Creates the SQLAlchemy engine.

The engine is the main database connection manager.

Example:

```python
engine = create_engine(DATABASE_URL)
```

Engine means:

```txt
database connection setup
```

---

## `SessionLocal`

`SessionLocal` is a session factory.

It creates database sessions.

Example:

```python
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
```

Engine = connection manager.

Session = one working conversation with the database.

---

## Session

A session is one temporary work session with the database.

Example:

When someone calls:

```txt
POST /projects
```

FastAPI opens a session, creates the project, saves it, then closes the session.

---

## Base

`Base` is the parent class for SQLAlchemy models.

Example:

```python
Base = declarative_base()
```

Then:

```python
class Project(Base):
    ...
```

means:

This Python class maps to a database table.

---

## `get_db()`

`get_db()` opens a database session, gives it to the route, and closes it after the route finishes.

Example:

```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

`yield` means:

Give this value to the route, but resume later for cleanup.

`finally` means:

Always run this cleanup code.

---

## SQLAlchemy Model

A SQLAlchemy model is a Python class that maps to a database table.

Example:

```python
class Project(Base):
    __tablename__ = "projects"

    id = ...
    title = ...
    description = ...
```

---

## `__tablename__`

Defines the database table name.

Example:

```python
__tablename__ = "projects"
```

Means:

This model maps to the `projects` table.

---

## Primary Key

A primary key is the unique identifier for each row.

Example:

```python
id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
```

---

## Project Model

Fields:

```txt
id
title
description
created_at
updated_at
```

Purpose:

Stores research projects in the database.

---

## `created_at` and `updated_at`

Used for timestamps.

`created_at`

When row was created.

`updated_at`

When row was last updated.

---

## `Base.metadata.create_all(bind=engine)`

Creates database tables for all known models.

Important:

SQLAlchemy only knows about models that have been imported.

That is why `main.py` imports models:

```python
from app import models
```

Then:

```python
Base.metadata.create_all(bind=engine)
```

means:

Look at every model class inheriting from `Base`, then create missing tables.

---

## Inspect Postgres with `psql`

Run command inside the Postgres container:

```bash
docker compose exec postgres psql -U postgres -d venture_agent
```

Meaning:

* `docker compose exec` = run a command inside an already-running container
* `postgres` = service/container name
* `psql` = Postgres command-line client
* `-U postgres` = use Postgres role/user named `postgres`
* `-d venture_agent` = connect to database named `venture_agent`

---

## Useful `psql` Commands

List tables:

```sql
\dt
```

Describe table:

```sql
\d projects
```

Describe users table:

```sql
\d users
```

List roles/users:

```sql
\du
```

List databases:

```sql
\l
```

Quit:

```sql
\q
```

---

## Pydantic Schema

A Pydantic schema defines the shape of data going into and out of the API.

SQLAlchemy model = database shape.

Pydantic schema = request/response shape.

---

## Project Schemas

`ProjectBase`

Common project fields.

```python
class ProjectBase(BaseModel):
    title: str
    description: str | None = None
```

`ProjectCreate`

Request body for creating a project.

```python
class ProjectCreate(ProjectBase):
    pass
```

`ProjectRead`

Response shape for returning a project.

Includes database-generated fields:

```txt
id
created_at
updated_at
```

`ProjectUpdate`

Request body for updating a project.

Fields are optional because PATCH may update only one field.

```python
class ProjectUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
```

---

## `ConfigDict(from_attributes=True)`

Allows Pydantic to read from SQLAlchemy model objects.

Used in response schemas.

Example:

```python
model_config = ConfigDict(from_attributes=True)
```

---

## FastAPI Router

A router groups related routes into a separate file.

Example:

```txt
backend/app/routers/projects.py
```

Purpose:

Keep project routes separate from `main.py`.

---

## `APIRouter`

Creates a group of routes.

Example:

```python
router = APIRouter(prefix="/projects", tags=["projects"])
```

`prefix="/projects"`

All routes in this router start with `/projects`.

`tags=["projects"]`

Groups routes in FastAPI docs.

---

## `include_router`

Connects a router to the main FastAPI app.

Example:

```python
app.include_router(projects.router)
```

Without this, routes in `projects.py` do not appear in `/docs`.

---

## CRUD Route Concepts

`db.add()`

Stage a new database object.

```python
db.add(project)
```

---

`db.commit()`

Save changes to the database.

```python
db.commit()
```

---

`db.refresh()`

Reload database-generated values like `id`, `created_at`, `updated_at`.

```python
db.refresh(project)
```

---

`db.delete()`

Delete a database object.

```python
db.delete(project)
```

---

`.all()`

Return all matching rows.

```python
db.query(models.Project).all()
```

---

`.first()`

Return the first matching row or `None`.

```python
db.query(models.Project).filter(models.Project.id == project_id).first()
```

---

`HTTPException`

Lets the API return an HTTP error.

Example:

```python
raise HTTPException(status_code=404, detail="Project not found")
```

---

`exclude_unset=True`

Used for PATCH.

Only updates fields the user actually sent.

Example:

```python
update_data = project_update.model_dump(exclude_unset=True)
```

Without it, missing fields could overwrite existing values with `None`.

---

## Day 2 Summary

Completed:

* Created branch `feature/projects-crud`
* Installed SQLAlchemy, psycopg2-binary, python-dotenv
* Created `backend/app/database.py`
* Added `DATABASE_URL`
* Added SQLAlchemy engine
* Added `SessionLocal`
* Added `Base`
* Added `get_db()`
* Fixed local vs Docker database URLs
* Created `Project` SQLAlchemy model
* Created `projects` table
* Created project Pydantic schemas
* Created projects router
* Added full Projects CRUD:

  * `POST /projects`
  * `GET /projects`
  * `GET /projects/{project_id}`
  * `PATCH /projects/{project_id}`
  * `DELETE /projects/{project_id}`
* Connected router in `main.py`
* Tested routes in `/docs`
* Updated README
* Pushed and merged Day 2 into `main`

---

# Day 3 — Authentication Basics with Users, Password Hashing, and JWT

## Goal

Add basic authentication:

* user model
* users table
* user schemas
* password hashing
* register route
* login route
* JWT token creation
* token decoding
* current user dependency
* `/auth/me`
* automated tests

Not done yet:

* connect projects to users
* protect project routes
* refresh tokens
* logout
* production-ready auth
* frontend auth

---

## Authentication Pieces

User model:

Database representation of a user.

Password hashing:

Protects passwords by storing a one-way hash instead of the real password.

Register route:

Creates a new user.

Login route:

Checks email/password and returns a JWT if correct.

JWT token:

A signed token used to prove the user is logged in on future requests.

---

## User Model

A `User` model is the database version of an app user.

Fields:

```txt
id
email
hashed_password
created_at
updated_at
```

Important:

Never store real passwords.

Store only `hashed_password`.

---

## `unique=True`

Example:

```python
email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
```

`unique=True` means two users cannot have the same email.

This helps prevent duplicate accounts.

---

## `hashed_password`

Stores the protected password hash.

Example:

```python
hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
```

Do not call the column `password`.

Do not store the plain password.

---

## Type Hint vs Database Column Type

Example:

```python
email: Mapped[str] = mapped_column(String(255))
```

`Mapped[str]`

Python-side type hint.

Means Python treats email as a string.

`String(255)`

Database-side column type.

Means Postgres stores it as a varchar/text column with max length 255.

Bad mismatch example:

```python
email: Mapped[int] = mapped_column(String(255))
```

This is wrong because Python says integer but database says string.

---

## Users Table

After adding the `User` model, `Base.metadata.create_all(bind=engine)` creates the `users` table if the model is imported.

Verified in Postgres with:

```sql
\dt
```

Expected tables:

```txt
projects
users
```

Describe users table:

```sql
\d users
```

Expected columns:

```txt
id
email
hashed_password
created_at
updated_at
```

---

## Postgres Role Issue

Tried:

```bash
docker compose exec postgres psql -U venture_user -d venture_agent
```

Error:

```txt
FATAL: role "venture_user" does not exist
```

Reason:

Current `.env` uses:

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=venture_agent
```

So the correct command is:

```bash
docker compose exec postgres psql -U postgres -d venture_agent
```

Lesson:

Use the database username from `.env`.

---

## Pydantic User Schemas

User schemas added:

```txt
UserCreate
UserLogin
UserRead
Token
```

---

## `UserCreate`

Used when registering.

Includes plain password because the user must send it.

```python
class UserCreate(BaseModel):
    email: str
    password: str
```

---

## `UserLogin`

Used when logging in.

Also includes plain password because the user must prove they know it.

```python
class UserLogin(BaseModel):
    email: str
    password: str
```

---

## `UserRead`

Used when returning user data.

Does not include `password`.

Does not include `hashed_password`.

```python
class UserRead(BaseModel):
    id: int
    email: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
```

Important auth rule:

```txt
password comes in
hashed_password gets stored
password and hashed_password never get returned
```

---

## `Token`

Used for login response.

```python
class Token(BaseModel):
    access_token: str
    token_type: str
```

Example response:

```json
{
  "access_token": "eyJ...",
  "token_type": "bearer"
}
```

---

## Password Hashing

Password hashing converts a real password into a one-way protected hash.

Example plain password:

```txt
password123
```

Stored hash:

```txt
$argon2id$v=19$...
```

Important:

A hash should not be reversed or decoded.

During registration:

```txt
plain password -> hash -> store hash
```

During login:

```txt
plain submitted password + stored hash -> verify true/false
```

---

## `pwdlib`

`pwdlib` is used for password hashing.

Installed:

```bash
pip install "pwdlib[argon2]"
```

Added to `requirements.txt`:

```txt
pwdlib[argon2]
```

---

## `security.py`

Created:

```txt
backend/app/security.py
```

Purpose:

Store reusable security helper functions.

Why:

Routes should call helper functions instead of containing all hashing/JWT logic directly.

---

## `PasswordHash.recommended()`

Sets up a recommended password hashing configuration.

Example:

```python
password_hasher = PasswordHash.recommended()
```

---

## `hash_password()`

Used during registration.

```python
def hash_password(password: str) -> str:
    return password_hasher.hash(password)
```

Takes a plain password.

Returns a hash.

---

## `verify_password()`

Used during login.

```python
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hasher.verify(plain_password, hashed_password)
```

Compares the submitted password against the stored hash.

Returns `True` or `False`.

---

## Auth Router

Created:

```txt
backend/app/routers/auth.py
```

Auth routes:

```txt
POST /auth/register
POST /auth/login
GET /auth/me
```

Router:

```python
router = APIRouter(prefix="/auth", tags=["auth"])
```

---

## Register Route

Endpoint:

```txt
POST /auth/register
```

Flow:

```txt
receive email/password
check if email already exists
hash password
save user with hashed_password
return safe UserRead response
```

Important:

The route receives `password`.

It stores `hashed_password`.

It returns `UserRead`.

---

## `status.HTTP_201_CREATED`

Registration uses status code `201`.

Meaning:

A new resource was created.

Example:

```python
@router.post("/register", response_model=schemas.UserRead, status_code=status.HTTP_201_CREATED)
```

---

## `response_model=schemas.UserRead`

This tells FastAPI to return only the fields allowed by `UserRead`.

Even if the SQLAlchemy `User` object has `hashed_password`, the API response does not include it.

This is a safety layer.

---

## Duplicate Registration

If email already exists:

```json
{
  "detail": "Email already registered"
}
```

Status:

```txt
400 Bad Request
```

Reason:

The user is trying to create an account with an already-used email.

---

## Login Route Before JWT

Initial login returned:

```json
{
  "message": "Login successful"
}
```

This proved password verification worked before adding tokens.

---

## Login Route with JWT

Endpoint:

```txt
POST /auth/login
```

Flow:

```txt
receive email/password
find user by email
verify submitted password against stored hash
create JWT token
return token
```

Response:

```json
{
  "access_token": "eyJ...",
  "token_type": "bearer"
}
```

---

## `401 Unauthorized`

Used for failed login.

Examples:

* missing user
* wrong password
* invalid token
* expired token

Bad login response:

```json
{
  "detail": "Invalid email or password"
}
```

Important:

Use the same error message for missing email and wrong password.

Do not say:

```txt
email not found
```

or:

```txt
wrong password
```

because that helps attackers guess which emails are registered.

---

## JWT

JWT means JSON Web Token.

It is a signed token that proves the user logged in.

After login, instead of sending email/password on every request, the frontend sends the token.

---

## Signed Token

A signed token is created using a secret key.

The frontend can hold the token.

But it cannot safely fake a new valid token unless it knows the secret key.

Important:

```txt
password proves identity once during login
JWT proves identity on later requests
SECRET_KEY signs the JWT
```

---

## PyJWT

PyJWT is used to create and decode JWTs.

Installed:

```bash
pip install PyJWT
```

Added to `requirements.txt`:

```txt
PyJWT
```

---

## JWT Config

Added to `.env`:

```env
SECRET_KEY=dev_secret_key_32_bytes_minimum_change_later
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Added to `.env.example`:

```env
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

## `SECRET_KEY`

Private string used to sign JWTs.

Important:

Do not commit real secret keys.

`.env` gets the real local value.

`.env.example` gets a fake placeholder.

For HS256, the key should be at least 32 bytes to avoid insecure key length warnings.

---

## `ALGORITHM=HS256`

JWT signing algorithm.

HS256 uses the same secret key to sign and verify the token.

---

## `ACCESS_TOKEN_EXPIRE_MINUTES`

Controls how long the access token is valid.

Example:

```env
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Means token expires after 30 minutes.

Why:

Old tokens should eventually stop working.

---

## JWT Payload

The payload is the data inside the token.

Example:

```python
{"sub": "joe@example.com"}
```

`sub` means subject.

In auth, it means who the token belongs to.

For now, the app uses email as the subject.

Later, using user ID may be better.

---

## `exp`

JWT expiration claim.

Example:

```python
payload.update({"exp": expire_time})
```

Means:

This token expires at this time.

---

## `jwt.encode`

Creates a signed token.

```python
token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
```

Meaning:

```txt
payload + secret key + algorithm = signed JWT
```

---

## `create_access_token()`

Used during login.

```python
def create_access_token(data: dict) -> str:
    payload = data.copy()

    expire_time = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload.update({"exp": expire_time})

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return token
```

---

## Bearer Token

`bearer` means:

Whoever carries this token can use it as proof of login.

Future request header:

```txt
Authorization: Bearer eyJ...
```

In login response:

```json
{
  "access_token": "...",
  "token_type": "bearer"
}
```

---

## JWT Decoding

The backend must create tokens and also verify/read tokens.

Create during login.

Decode during protected requests.

---

## `decode_access_token()`

```python
def decode_access_token(token: str) -> dict | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.InvalidTokenError:
        return None
```

What it does:

* reads the token
* checks the signature
* checks expiration
* returns payload if valid
* returns `None` if invalid/expired/fake

---

## Authorization Header

HTTP headers are extra metadata sent with a request.

For auth:

```txt
Authorization: Bearer <token>
```

This carries the login token.

---

## Auth Dependency

Created:

```txt
backend/app/dependencies.py
```

Purpose:

Reusable route logic for getting the current logged-in user.

---

## `HTTPBearer`

Reads the bearer token from the Authorization header.

Example:

```python
bearer_scheme = HTTPBearer()
```

---

## `get_current_user()`

Flow:

```txt
read token from Authorization header
decode token
get email from token payload sub
look up user in database
return user
```

Why load from database:

Do not trust only the token.

The user may have been deleted or changed.

The database is the source of truth.

---

## Protected Route

A protected route requires valid auth before it runs.

Example:

```python
current_user: models.User = Depends(get_current_user)
```

Means:

Before this route runs, FastAPI must verify the token and load the user.

---

## `/auth/me`

Endpoint:

```txt
GET /auth/me
```

Returns the currently logged-in user.

Requires:

```txt
Authorization: Bearer <token>
```

Response:

```json
{
  "id": 1,
  "email": "joe@example.com",
  "created_at": "...",
  "updated_at": "..."
}
```

No token:

```json
{
  "detail": "Not authenticated"
}
```

or depending on FastAPI version/config:

```json
{
  "detail": "Not authenticated"
}
```

Status may be `401` or `403` depending on `HTTPBearer` behavior.

---

## Full Day 3 Auth Flow

```txt
1. User registers with email/password.
2. Backend checks if email already exists.
3. Backend hashes password.
4. Backend stores user with hashed_password.
5. User logs in with email/password.
6. Backend finds user by email.
7. Backend verifies password against stored hash.
8. Backend creates JWT with sub=email and exp=expiration time.
9. Backend returns access_token and token_type=bearer.
10. Client sends Authorization: Bearer <token>.
11. Backend decodes token.
12. Backend loads user from database.
13. Protected route returns current user.
```

---

# Testing

## Test Setup

Tests use:

```txt
backend/tests/test_api.py
```

Testing tool:

```txt
pytest
```

FastAPI testing tool:

```txt
TestClient
```

---

## SQLite Test Database

Tests use temporary SQLite instead of requiring Postgres.

Why:

* faster
* isolated
* does not require Docker/Postgres running
* safer for automated tests

Test database URL:

```python
os.environ["DATABASE_URL"] = f"sqlite:///{tmp_db_path}"
```

Important:

Set environment variables before importing `app.main`, because `database.py` reads `DATABASE_URL` during import.

---

## Test JWT Environment

Tests set their own JWT config:

```python
os.environ["SECRET_KEY"] = "test_secret_key_32_bytes_minimum!!"
os.environ["ALGORITHM"] = "HS256"
os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"] = "30"
```

Why:

Tests should not depend on the real `.env`.

---

## Test Import Path

Use:

```bash
PYTHONPATH=backend .venv/bin/pytest backend/tests -q
```

`PYTHONPATH=backend` tells Python:

Treat `backend/` as an import root.

That makes this work:

```python
from app.main import app
```

---

## Import Style Rule

Use this style inside backend code:

```python
from app import models
from app.database import Base, engine
from app.routers import projects, auth
```

Avoid mixing with:

```python
from backend.app import models
```

Reason:

The app is run from inside the backend package context where `app` is the package.

Mixed imports can cause:

```txt
ModuleNotFoundError: No module named 'backend'
```

---

## Reset Test Database Before Each Test

Tests drop and recreate tables before each test.

Purpose:

Tests should not depend on test order.

Each test starts with a clean database.

---

## Tests Currently Passing

Current test result:

```txt
10 passed
```

Tests cover:

* health route
* projects CRUD
* user registration
* duplicate email failure
* password stored hashed, not plain text
* login returns JWT
* wrong password fails
* missing user fails
* `/auth/me` with valid token
* `/auth/me` without token fails

---

## Useful Test Command

Run tests:

```bash
PYTHONPATH=backend .venv/bin/pytest backend/tests -q
```

Expected:

```txt
10 passed
```

---

# Current API Endpoints

## Health

```txt
GET /health
```

Returns:

```json
{
  "status": "ok"
}
```

---

## Projects

```txt
POST /projects
GET /projects
GET /projects/{project_id}
PATCH /projects/{project_id}
DELETE /projects/{project_id}
```

Projects are not connected to users yet.

Project routes are not protected yet.

---

## Auth

```txt
POST /auth/register
POST /auth/login
GET /auth/me
```

---

# Current Project State

Day 1 complete:

FastAPI backend, Docker, Compose, Postgres, GitHub.

Day 2 complete:

Projects CRUD with SQLAlchemy/Postgres.

Day 3 auth basics complete locally:

* users table
* password hashing
* registration
* login
* JWT creation
* JWT decoding
* current user dependency
* `/auth/me`
* automated tests passing

Important:

Local Day 3 is working.

Make sure Day 3 files are committed and pushed to GitHub.

---

# What Day 3 Does Not Include Yet

Still future work:

* connect projects to users
* add `owner_id` to projects
* protect project routes
* make users only see their own projects
* add Alembic migrations
* add email validation with `EmailStr`
* add password strength rules
* add refresh tokens
* add logout/token invalidation
* add frontend auth flow
* add GitHub Actions CI
* deploy backend/database
* add RAG/vector search
* add document upload
* add report generation

---

# Git Commands for Day 3 Finish

Check status:

```bash
git status
```

Make sure `.env` is not staged.

Add Day 3 files:

```bash
git add backend/app/models.py backend/app/schemas.py backend/app/security.py backend/app/dependencies.py backend/app/routers/auth.py backend/app/main.py backend/requirements.txt backend/tests/test_api.py README.md .env.example
```

Commit:

```bash
git commit -m "Add authentication basics with JWT"
```

Push:

```bash
git push
```

---

# Mental Model Summary

FastAPI:

Defines API routes.

Uvicorn:

Runs the FastAPI app.

Dockerfile:

Recipe for packaging backend.

Docker image:

Packaged app environment.

Docker container:

Running image.

Docker Compose:

Runs backend + Postgres together.

Postgres:

Stores persistent app data.

Volume:

Keeps database data after containers restart.

`.env`:

Real local config/secrets. Do not commit.

`.env.example`:

Safe config template. Commit.

SQLAlchemy model:

Database table shape.

Pydantic schema:

API input/output shape.

Database session:

One temporary conversation with the database.

Router:

Groups related routes.

`include_router`:

Connects route group to app.

Password hash:

One-way protected password storage.

JWT:

Signed login token.

Bearer token:

Token carried in Authorization header.

`get_current_user`:

Reusable dependency that verifies token and loads user.

`/auth/me`:

Proof that the token pipeline works.

Tests:

Proof that current behavior keeps working.
