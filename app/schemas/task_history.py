from pydantic import BaseModel
from datetime import datetime
from app.schemas.user import UserInDB
from app.schemas.task import TaskInDB

class TaskHistoryBase(BaseModel):
    change_type: str
    old_value: Optional[str] = None
    new_value: Optional[str] = None

class TaskHistoryInDB(TaskHistoryBase):
    id: int
    task_id: int
    changed_by: int
    changed_at: datetime
    task: TaskInDB
    user: UserInDB

    class Config:
        from_attributes = True