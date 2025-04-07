from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from app.schemas.project import ProjectInDB
from app.schemas.user import UserInDB

class BoardColumnBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    position: int

class BoardColumnCreate(BoardColumnBase):
    pass

class BoardColumnInDB(BoardColumnBase):
    id: int
    board_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class BoardBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    project_id: int

class BoardCreate(BoardBase):
    columns: List[BoardColumnCreate] = []

class BoardUpdate(BaseModel):
    name: Optional[str] = None

class BoardInDB(BoardBase):
    id: int
    created_by: int
    created_at: datetime
    updated_at: datetime
    project: ProjectInDB
    creator: UserInDB
    columns: List[BoardColumnInDB] = []

    class Config:
        from_attributes = True