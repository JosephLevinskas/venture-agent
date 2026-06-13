from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ProjectBase(BaseModel):
    title: str
    description: str | None = None

class ProjectCreate(ProjectBase):
    pass

class ProjectRead(ProjectBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ProjectUpdate(BaseModel):
    title: str | None = None
    description: str | None = None

class UserCreate(BaseModel):
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserRead(BaseModel):
    id: int
    email: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str