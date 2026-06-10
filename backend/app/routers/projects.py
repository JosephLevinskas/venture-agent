from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

router = APIRouter() # creates route group 

@router.post("/projects", response_model=schemas.ProjectRead)
def create_project(project: schemas.ProjectCreate, db: Session = Depends(get_db)):
    db_project = models.Project(title=project.title, description=project.description)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

@router.get("/projects", response_model=list[schemas.ProjectRead])
def list_projects(db: Session = Depends(get_db)):
    projects = db.query(models.Project).all()

    return projects

@router.get("/projects/{project_id}", response_model=schemas.ProjectRead)
def get_project(
    project_id: int,
    db: Session = Depends(get_db),
):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()

    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")

    return project

@router.patch("/projects/{project_id}", response_model=schemas.ProjectRead)
def update_project(
    project_id: int,
    project_update: schemas.ProjectUpdate,
    db: Session = Depends(get_db),
):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()

    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")

    update_data = project_update.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(project, field, value)

    db.commit()
    db.refresh(project)

    return project

@router.delete("/projects/{project_id}")
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()

    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")

    db.delete(project)
    db.commit()

    return {"message": "Project deleted successfully"}