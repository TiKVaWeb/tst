from pydantic import BaseModel
from datetime import datetime
from app.schemas.user import UserInDB
from app.schemas.project import ProjectInDB

class ProjectMemberBase(BaseModel):
    role: str

class ProjectMemberCreate(ProjectMemberBase):
    user_id: int

class ProjectMemberUpdate(ProjectMemberBase):
    pass

class ProjectMemberInDB(ProjectMemberBase):
    id: int
    project_id: int
    user_id: int
    joined_at: datetime
    member: UserInDB
    project: ProjectInDB

    class Config:
        from_attributes = True