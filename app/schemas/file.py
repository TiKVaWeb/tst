from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.schemas.user import UserInDB
from app.schemas.project import ProjectInDB
from app.schemas.task import TaskInDB

class ProjectFileBase(BaseModel):
    name: str
    size: int
    mime_type: Optional[str] = None

class ProjectFileCreate(ProjectFileBase):
    pass

class ProjectFileInDB(ProjectFileBase):
    id: int
    project_id: int
    uploaded_by: int
    version_number: int
    is_current: bool
    created_at: datetime
    updated_at: datetime
    project: ProjectInDB
    uploader: UserInDB

    class Config:
        from_attributes = True

class TaskAttachmentInDB(BaseModel):
    id: int
    task_id: int
    file_id: int
    uploaded_by: int
    created_at: datetime
    task: TaskInDB
    file: ProjectFileInDB
    uploader: UserInDB

    class Config:
        from_attributes = True