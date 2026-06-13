from pathlib import Path
import sys
import os
import importlib
import tempfile
import atexit

import pytest
from fastapi.testclient import TestClient


# Ensure the backend/ folder is on sys.path so `import app` works
backend_path = Path(__file__).resolve().parents[1]
if str(backend_path) not in sys.path:
    sys.path.insert(0, str(backend_path))


# Use a temporary SQLite database for tests instead of requiring Postgres
tmp_db = tempfile.NamedTemporaryFile(prefix="test_db_", suffix=".sqlite", delete=False)
tmp_db_path = tmp_db.name
tmp_db.close()

os.environ["DATABASE_URL"] = f"sqlite:///{tmp_db_path}"

# Test-only JWT settings
os.environ["SECRET_KEY"] = "test_secret_key"
os.environ["ALGORITHM"] = "HS256"
os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"] = "30"


def _cleanup_tmp_db():
    try:
        os.remove(tmp_db_path)
    except OSError:
        pass


atexit.register(_cleanup_tmp_db)

importlib.invalidate_caches()

from app.main import app
from app import database, models


client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_test_database():
    """
    Reset all tables before each test so tests do not depend on order.
    """
    database.Base.metadata.drop_all(bind=database.engine)
    database.Base.metadata.create_all(bind=database.engine)
    yield


def test_health():
    r = client.get("/health")

    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_project_crud_flow():
    # Start with empty list
    r = client.get("/projects")
    assert r.status_code == 200
    assert r.json() == []

    # Create project
    payload = {
        "title": "Test Project",
        "description": "a test",
    }

    r = client.post("/projects", json=payload)
    assert r.status_code == 200

    created = r.json()
    assert created["title"] == payload["title"]
    assert created["description"] == payload["description"]
    assert "id" in created
    assert "created_at" in created
    assert "updated_at" in created

    project_id = created["id"]

    # List contains created project
    r = client.get("/projects")
    assert r.status_code == 200

    projects = r.json()
    assert any(project["id"] == project_id for project in projects)

    # Get single project
    r = client.get(f"/projects/{project_id}")
    assert r.status_code == 200

    one = r.json()
    assert one["id"] == project_id
    assert one["title"] == payload["title"]

    # Patch project
    r = client.patch(f"/projects/{project_id}", json={"title": "Updated"})
    assert r.status_code == 200

    updated = r.json()
    assert updated["id"] == project_id
    assert updated["title"] == "Updated"
    assert updated["description"] == payload["description"]

    # Delete project
    r = client.delete(f"/projects/{project_id}")
    assert r.status_code == 200
    assert r.json().get("message") == "Project deleted successfully"

    # Deleted project should return 404
    r = client.get(f"/projects/{project_id}")
    assert r.status_code == 404


def test_register_user():
    payload = {
        "email": "joe@example.com",
        "password": "password123",
    }

    r = client.post("/auth/register", json=payload)
    assert r.status_code == 201

    created = r.json()
    assert created["email"] == payload["email"]
    assert "id" in created
    assert "created_at" in created
    assert "updated_at" in created

    # API should never return password fields
    assert "password" not in created
    assert "hashed_password" not in created


def test_register_duplicate_email_fails():
    payload = {
        "email": "joe@example.com",
        "password": "password123",
    }

    first = client.post("/auth/register", json=payload)
    assert first.status_code == 201

    second = client.post("/auth/register", json=payload)
    assert second.status_code == 400
    assert second.json()["detail"] == "Email already registered"


def test_register_stores_hashed_password_not_plain_password():
    payload = {
        "email": "joe@example.com",
        "password": "password123",
    }

    r = client.post("/auth/register", json=payload)
    assert r.status_code == 201

    db = database.SessionLocal()
    try:
        user = db.query(models.User).filter(models.User.email == payload["email"]).first()

        assert user is not None
        assert user.hashed_password != payload["password"]
        assert user.hashed_password.startswith("$argon2")
    finally:
        db.close()


def test_login_returns_jwt_token():
    payload = {
        "email": "joe@example.com",
        "password": "password123",
    }

    register_response = client.post("/auth/register", json=payload)
    assert register_response.status_code == 201

    login_response = client.post("/auth/login", json=payload)
    assert login_response.status_code == 200

    body = login_response.json()

    assert "access_token" in body
    assert body["access_token"].startswith("eyJ")
    assert body["token_type"] == "bearer"


def test_login_wrong_password_fails():
    register_payload = {
        "email": "joe@example.com",
        "password": "password123",
    }

    client.post("/auth/register", json=register_payload)

    wrong_login_payload = {
        "email": "joe@example.com",
        "password": "wrongpassword",
    }

    r = client.post("/auth/login", json=wrong_login_payload)

    assert r.status_code == 401
    assert r.json()["detail"] == "Invalid email or password"


def test_login_missing_user_fails():
    payload = {
        "email": "missing@example.com",
        "password": "password123",
    }

    r = client.post("/auth/login", json=payload)

    assert r.status_code == 401
    assert r.json()["detail"] == "Invalid email or password"


def test_auth_me_with_valid_token_returns_current_user():
    payload = {
        "email": "joe@example.com",
        "password": "password123",
    }

    register_response = client.post("/auth/register", json=payload)
    assert register_response.status_code == 201

    login_response = client.post("/auth/login", json=payload)
    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    me_response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert me_response.status_code == 200

    body = me_response.json()
    assert body["email"] == payload["email"]
    assert "id" in body
    assert "created_at" in body
    assert "updated_at" in body

    # API should never return password fields
    assert "password" not in body
    assert "hashed_password" not in body


def test_auth_me_without_token_fails():
    r = client.get("/auth/me")

    # FastAPI HTTPBearer may return 401 or 403 depending on version/config
    assert r.status_code in (401, 403)