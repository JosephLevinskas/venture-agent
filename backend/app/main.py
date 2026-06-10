from fastapi import FastAPI

from app import models
from app.database import Base, engine
from app.routers import projects

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(projects.router)

@app.get("/health")
def health():
    return {"status": "ok"}