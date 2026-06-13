from pathlib import Path
import sys
import os
import importlib
import tempfile
import atexit

import pytest
from fastapi.testclient import TestClient


# Ensure backend/ is on sys.path so `import app` works
backend_path = Path(__file__).resolve().parents[1]
if str(backend_path) not in sys.path:
    sys.path.insert(0, str(backend_path))


# Use a temporary SQLite database for this test file if app is imported fresh
tmp_db = tempfile.NamedTemporaryFile(prefix="test_day4_db_", suffix=".sqlite", delete=False)
tmp_db_path = tmp_db.name
tmp_db.close()

os.environ["DATABASE_URL"] = f"sqlite:///{tmp_db_path}"
os.environ["SECRET_KEY"] = "test_secret_key_for_day4"
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


def get_auth_headers(email="projectowner@example.com", password="testpassword123"):
    register_response = client.post(
        "/auth/register",
        json={
            "email": email,
            "password": password,
        },
    )
    assert register_response.status_code == 201

    login_response = client.post(
        "/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )
    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    return {"Authorization": f"Bearer {token}"}


def create_project(headers, title="Test Project", description="a test project"):
    response = client.post(
        "/projects",
        json={
            "title": title,
            "description": description,
        },
        headers=headers,
    )

    assert response.status_code == 200

    return response.json()


def test_project_routes_require_authentication():
    create_response = client.post(
        "/projects",
        json={
            "title": "No Auth Project",
            "description": "should fail",
        },
    )
    assert create_response.status_code in (401, 403)

    list_response = client.get("/projects")
    assert list_response.status_code in (401, 403)

    get_response = client.get("/projects/1")
    assert get_response.status_code in (401, 403)

    patch_response = client.patch(
        "/projects/1",
        json={"title": "Should Fail"},
    )
    assert patch_response.status_code in (401, 403)

    delete_response = client.delete("/projects/1")
    assert delete_response.status_code in (401, 403)


def test_create_project_assigns_owner_id_from_logged_in_user():
    headers = get_auth_headers(email="owner@example.com")

    created = create_project(
        headers=headers,
        title="Owned Project",
        description="created by logged-in user",
    )

    assert created["title"] == "Owned Project"
    assert created["description"] == "created by logged-in user"
    assert "id" in created
    assert "owner_id" in created
    assert created["owner_id"] > 0
    assert "created_at" in created
    assert "updated_at" in created

    db = database.SessionLocal()
    try:
        user = db.query(models.User).filter(models.User.email == "owner@example.com").first()
        project = db.query(models.Project).filter(models.Project.id == created["id"]).first()

        assert user is not None
        assert project is not None
        assert project.owner_id == user.id
    finally:
        db.close()


def test_list_projects_only_returns_current_users_projects():
    user_one_headers = get_auth_headers(email="userone@example.com")
    user_two_headers = get_auth_headers(email="usertwo@example.com")

    user_one_project = create_project(
        headers=user_one_headers,
        title="User One Project",
        description="belongs to user one",
    )

    create_project(
        headers=user_two_headers,
        title="User Two Project",
        description="belongs to user two",
    )

    response = client.get("/projects", headers=user_one_headers)

    assert response.status_code == 200

    projects = response.json()

    assert len(projects) == 1
    assert projects[0]["id"] == user_one_project["id"]
    assert projects[0]["title"] == "User One Project"
    assert projects[0]["owner_id"] == user_one_project["owner_id"]


def test_get_project_only_allows_owner():
    owner_headers = get_auth_headers(email="getowner@example.com")
    other_user_headers = get_auth_headers(email="getother@example.com")

    created = create_project(
        headers=owner_headers,
        title="Private Get Project",
        description="only owner can get this",
    )

    project_id = created["id"]

    owner_response = client.get(
        f"/projects/{project_id}",
        headers=owner_headers,
    )

    assert owner_response.status_code == 200
    assert owner_response.json()["id"] == project_id
    assert owner_response.json()["title"] == "Private Get Project"

    other_response = client.get(
        f"/projects/{project_id}",
        headers=other_user_headers,
    )

    assert other_response.status_code == 404
    assert other_response.json()["detail"] == "Project not found"


def test_update_project_only_allows_owner():
    owner_headers = get_auth_headers(email="patchowner@example.com")
    other_user_headers = get_auth_headers(email="patchother@example.com")

    created = create_project(
        headers=owner_headers,
        title="Original Title",
        description="original description",
    )

    project_id = created["id"]

    other_update = client.patch(
        f"/projects/{project_id}",
        json={"title": "Hacked Title"},
        headers=other_user_headers,
    )

    assert other_update.status_code == 404
    assert other_update.json()["detail"] == "Project not found"

    owner_update = client.patch(
        f"/projects/{project_id}",
        json={"title": "Owner Updated Title"},
        headers=owner_headers,
    )

    assert owner_update.status_code == 200

    updated = owner_update.json()

    assert updated["id"] == project_id
    assert updated["title"] == "Owner Updated Title"
    assert updated["description"] == "original description"
    assert updated["owner_id"] == created["owner_id"]


def test_delete_project_only_allows_owner():
    owner_headers = get_auth_headers(email="deleteowner@example.com")
    other_user_headers = get_auth_headers(email="deleteother@example.com")

    created = create_project(
        headers=owner_headers,
        title="Delete Test Project",
        description="only owner can delete this",
    )

    project_id = created["id"]

    other_delete = client.delete(
        f"/projects/{project_id}",
        headers=other_user_headers,
    )

    assert other_delete.status_code == 404
    assert other_delete.json()["detail"] == "Project not found"

    owner_delete = client.delete(
        f"/projects/{project_id}",
        headers=owner_headers,
    )

    assert owner_delete.status_code == 200
    assert owner_delete.json()["message"] == "Project deleted successfully"

    owner_get_after_delete = client.get(
        f"/projects/{project_id}",
        headers=owner_headers,
    )

    assert owner_get_after_delete.status_code == 404


def test_project_owner_relationship_exists_in_database():
    headers = get_auth_headers(email="relationship@example.com")

    created = create_project(
        headers=headers,
        title="Relationship Test",
        description="testing user project relationship",
    )

    db = database.SessionLocal()
    try:
        project = db.query(models.Project).filter(models.Project.id == created["id"]).first()

        assert project is not None
        assert project.owner is not None
        assert project.owner.email == "relationship@example.com"

        user = db.query(models.User).filter(models.User.email == "relationship@example.com").first()

        assert user is not None
        assert len(user.projects) == 1
        assert user.projects[0].id == project.id
    finally:
        db.close()