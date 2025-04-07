from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from app.schemas.workspace import WorkspaceInDB
from app.schemas.user import UserInDB

class ProjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    workspace_id: int

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class ProjectInDB(ProjectBase):
    id: int
    created_by: int
    created_at: datetime
    updated_at: datetime
    workspace: WorkspaceInDB
    creator: UserInDB

    class Config:
        from_attributes = True