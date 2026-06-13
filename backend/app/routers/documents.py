from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..dependencies import get_current_user


router = APIRouter()


def get_owned_project(
    project_id: int,
    db: Session,
    current_user: models.User,
) -> models.Project:
    project = (
        db.query(models.Project)
        .filter(
            models.Project.id == project_id,
            models.Project.owner_id == current_user.id,
        )
        .first()
    )

    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")

    return project


def get_owned_document(
    document_id: int,
    db: Session,
    current_user: models.User,
) -> models.Document:
    document = (
        db.query(models.Document)
        .join(models.Project)
        .filter(
            models.Document.id == document_id,
            models.Project.owner_id == current_user.id,
        )
        .first()
    )

    if document is None:
        raise HTTPException(status_code=404, detail="Document not found")

    return document


@router.post(
    "/projects/{project_id}/documents",
    response_model=schemas.DocumentRead,
)
def create_document(
    project_id: int,
    document: schemas.DocumentCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    get_owned_project(project_id, db, current_user)

    db_document = models.Document(
        project_id=project_id,
        title=document.title,
        content=document.content,
    )

    db.add(db_document)
    db.commit()
    db.refresh(db_document)

    return db_document


@router.get(
    "/projects/{project_id}/documents",
    response_model=list[schemas.DocumentRead],
)
def list_documents_for_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    get_owned_project(project_id, db, current_user)

    documents = (
        db.query(models.Document)
        .filter(models.Document.project_id == project_id)
        .all()
    )

    return documents


@router.get("/documents/{document_id}", response_model=schemas.DocumentRead)
def get_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    document = get_owned_document(document_id, db, current_user)

    return document


@router.patch("/documents/{document_id}", response_model=schemas.DocumentRead)
def update_document(
    document_id: int,
    document_update: schemas.DocumentUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    document = get_owned_document(document_id, db, current_user)

    update_data = document_update.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(document, field, value)

    db.commit()
    db.refresh(document)

    return document


@router.delete("/documents/{document_id}")
def delete_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    document = get_owned_document(document_id, db, current_user)

    db.delete(document)
    db.commit()

    return {"message": "Document deleted successfully"}