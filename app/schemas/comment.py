from pydantic import BaseModel, Field
from datetime import datetime
from app.schemas.user import UserInDB
from app.schemas.task import TaskInDB

class CommentBase(BaseModel):
    content: str = Field(..., min_length=1)

class CommentCreate(CommentBase):
    pass

class CommentInDB(CommentBase):
    id: int
    task_id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    user: UserInDB
    task: TaskInDB

    class Config:
        from_attributes = True