from sqlalchemy import Column, Integer, Enum, Text, ForeignKey, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class TaskHistory(Base):
    __tablename__ = "task_history"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)
    changed_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    change_type = Column(Enum(
        'status', 'assignee', 'priority', 'due_date',
        'description', 'title', 'tag', 'attachment',
        'comment', 'column'
    ), nullable=False)
    old_value = Column(Text)
    new_value = Column(Text)
    changed_at = Column(TIMESTAMP, server_default=func.now())

    task = relationship("Task", back_populates="history")
    user = relationship("User")