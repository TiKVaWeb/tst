from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from app.schemas.user import UserInDB
from app.schemas.project import ProjectInDB
from app.schemas.board import BoardColumnInDB

class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    column_id: int
    assigned_to: Optional[int] = None
    priority: str = 'medium'
    due_date: Optional[datetime] = None

class TaskCreate(TaskBase):
    tag_ids: List[int] = []

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    column_id: Optional[int] = None
    assigned_to: Optional[int] = None
    priority: Optional[str] = None
    due_date: Optional[datetime] = None
    position: Optional[int] = None
    tag_ids: Optional[List[int]] = None

class TaskInDB(TaskBase):
    id: int
    project_id: int
    created_by: int
    position: int
    created_at: datetime
    updated_at: datetime
    project: ProjectInDB
    column: BoardColumnInDB
    creator: UserInDB
    assignee: Optional[UserInDB] = None
    tags: List[TagInDB] = []

    class Config:
        from_attributes = True

class TagBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    color: Optional[str] = None

class TagCreate(TagBase):
    pass

class TagInDB(TagBase):
    id: int
    project_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True