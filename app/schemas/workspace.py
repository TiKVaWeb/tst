from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from app.schemas.user import UserInDB

class WorkspaceBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None

class WorkspaceCreate(WorkspaceBase):
    pass

class WorkspaceUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class WorkspaceInDB(WorkspaceBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime
    owner: UserInDB

    class Config:
        from_attributes = True