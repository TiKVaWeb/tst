from sqlalchemy import Column, Integer, Enum, ForeignKey, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class ProjectMember(Base):
    __tablename__ = "project_members"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    role = Column(Enum('admin', 'member', 'viewer'), nullable=False, default='member')
    joined_at = Column(TIMESTAMP, server_default=func.now())

    project = relationship("Project", back_populates="members")
    member = relationship("User", back_populates="project_memberships")