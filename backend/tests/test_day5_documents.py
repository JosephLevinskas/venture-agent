from pathlib import Path
import sys
import os
import importlib
import tempfile
import atexit

import pytest
from fastapi.testclient import TestClient


backend_path = Path(__file__).resolve().parents[1]
if str(backend_path) not in sys.path:
    sys.path.insert(0, str(backend_path))


tmp_db = tempfile.NamedTemporaryFile(prefix="test_day5_db_", suffix=".sqlite", delete=False)
tmp_db_path = tmp_db.name
tmp_db.close()

os.environ["DATABASE_URL"] = f"sqlite:///{tmp_db_path}"
os.environ["SECRET_KEY"] = "test_secret_key_for_day5"
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
    database.Base.metadata.drop_all(bind=database.engine)
    database.Base.metadata.create_all(bind=database.engine)
    yield


def get_auth_headers(email="docowner@example.com", password="testpassword123"):
    register_response = client.post(
        "/auth/register",
        json={"email": email, "password": password},
    )
    assert register_response.status_code == 201

    login_response = client.post(
        "/auth/login",
        json={"email": email, "password": password},
    )
    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    return {"Authorization": f"Bearer {token}"}


def create_project(headers, title="Project With Docs"):
    response = client.post(
        "/projects",
        json={
            "title": title,
            "description": "project for document tests",
        },
        headers=headers,
    )
    assert response.status_code == 200
    return response.json()


def create_document(headers, project_id, title="Test Document", content="Test content"):
    response = client.post(
        f"/projects/{project_id}/documents",
        json={
            "title": title,
            "content": content,
        },
        headers=headers,
    )
    assert response.status_code == 200
    return response.json()


def test_document_routes_require_authentication():
    response = client.post(
        "/projects/1/documents",
        json={
            "title": "No Auth",
            "content": "should fail",
        },
    )
    assert response.status_code in (401, 403)

    response = client.get("/projects/1/documents")
    assert response.status_code in (401, 403)

    response = client.get("/documents/1")
    assert response.status_code in (401, 403)

    response = client.patch(
        "/documents/1",
        json={"title": "Should Fail"},
    )
    assert response.status_code in (401, 403)

    response = client.delete("/documents/1")
    assert response.status_code in (401, 403)


def test_create_document_attaches_to_owned_project():
    headers = get_auth_headers(email="docowner@example.com")
    project = create_project(headers)

    document = create_document(
        headers=headers,
        project_id=project["id"],
        title="Research Note",
        content="This is my first attached note.",
    )

    assert document["title"] == "Research Note"
    assert document["content"] == "This is my first attached note."
    assert document["project_id"] == project["id"]
    assert "id" in document
    assert "created_at" in document
    assert "updated_at" in document

    db = database.SessionLocal()
    try:
        db_document = (
            db.query(models.Document)
            .filter(models.Document.id == document["id"])
            .first()
        )

        assert db_document is not None
        assert db_document.project_id == project["id"]
    finally:
        db.close()


def test_cannot_create_document_on_another_users_project():
    owner_headers = get_auth_headers(email="projectowner@example.com")
    other_headers = get_auth_headers(email="otherdocuser@example.com")

    project = create_project(owner_headers, title="Private Project")

    response = client.post(
        f"/projects/{project['id']}/documents",
        json={
            "title": "Stolen Doc",
            "content": "should not attach",
        },
        headers=other_headers,
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Project not found"


def test_list_documents_only_for_owned_project():
    owner_headers = get_auth_headers(email="listdocowner@example.com")
    other_headers = get_auth_headers(email="listdocother@example.com")

    owner_project = create_project(owner_headers, title="Owner Project")
    other_project = create_project(other_headers, title="Other Project")

    owner_document = create_document(
        headers=owner_headers,
        project_id=owner_project["id"],
        title="Owner Note",
        content="owner content",
    )

    create_document(
        headers=other_headers,
        project_id=other_project["id"],
        title="Other Note",
        content="other content",
    )

    response = client.get(
        f"/projects/{owner_project['id']}/documents",
        headers=owner_headers,
    )

    assert response.status_code == 200

    documents = response.json()

    assert len(documents) == 1
    assert documents[0]["id"] == owner_document["id"]
    assert documents[0]["title"] == "Owner Note"

def test_get_document_only_allows_project_owner():
    owner_headers = get_auth_headers(email="getdocowner@example.com")
    other_headers = get_auth_headers(email="getdocother@example.com")

    project = create_project(owner_headers)
    document = create_document(owner_headers, project["id"])

    owner_response = client.get(
        f"/documents/{document['id']}",
        headers=owner_headers,
    )
    assert owner_response.status_code == 200
    assert owner_response.json()["id"] == document["id"]

    other_response = client.get(
        f"/documents/{document['id']}",
        headers=other_headers,
    )
    assert other_response.status_code == 404
    assert other_response.json()["detail"] == "Document not found"


def test_update_document_only_allows_project_owner():
    owner_headers = get_auth_headers(email="updatedocowner@example.com")
    other_headers = get_auth_headers(email="updatedocother@example.com")

    project = create_project(owner_headers)
    document = create_document(
        headers=owner_headers,
        project_id=project["id"],
        title="Original Doc",
        content="original content",
    )

    other_update = client.patch(
        f"/documents/{document['id']}",
        json={"title": "Hacked Doc"},
        headers=other_headers,
    )
    assert other_update.status_code == 404

    owner_update = client.patch(
        f"/documents/{document['id']}",
        json={"title": "Updated Doc"},
        headers=owner_headers,
    )
    assert owner_update.status_code == 200
    assert owner_update.json()["title"] == "Updated Doc"
    assert owner_update.json()["content"] == "original content"


def test_delete_document_only_allows_project_owner():
    owner_headers = get_auth_headers(email="deletedocowner@example.com")
    other_headers = get_auth_headers(email="deletedocother@example.com")

    project = create_project(owner_headers)
    document = create_document(owner_headers, project["id"])

    other_delete = client.delete(
        f"/documents/{document['id']}",
        headers=other_headers,
    )
    assert other_delete.status_code == 404

    owner_delete = client.delete(
        f"/documents/{document['id']}",
        headers=owner_headers,
    )
    assert owner_delete.status_code == 200
    assert owner_delete.json()["message"] == "Document deleted successfully"

    owner_get = client.get(
        f"/documents/{document['id']}",
        headers=owner_headers,
    )
    assert owner_get.status_code == 404


def test_deleting_project_deletes_attached_documents():
    headers = get_auth_headers(email="cascadeowner@example.com")

    project = create_project(headers)
    document = create_document(headers, project["id"])

    delete_project_response = client.delete(
        f"/projects/{project['id']}",
        headers=headers,
    )
    assert delete_project_response.status_code == 200

    db = database.SessionLocal()
    try:
        db_document = (
            db.query(models.Document)
            .filter(models.Document.id == document["id"])
            .first()
        )

        assert db_document is None
    finally:
        db.close()