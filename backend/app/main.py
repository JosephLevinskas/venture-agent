from fastapi import FastAPI

from app import models
from app.database import Base, engine
from app.routers import projects, auth, documents
from fastapi.middleware.cors import CORSMiddleware

# Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(projects.router)
app.include_router(auth.router)
app.include_router(documents.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}