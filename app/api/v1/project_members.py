from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.project import Project
from app.models.project_member import ProjectMember
from app.schemas.project_member import (
    ProjectMemberCreate,
    ProjectMemberInDB,
    ProjectMemberUpdate
)
from app.database import get_db
from app.utils.security import get_current_active_user

router = APIRouter(prefix="/projects/{project_id}/members", tags=["project_members"])


@router.post("/", response_model=ProjectMemberInDB)
def add_project_member(
        project_id: int,
        member: ProjectMemberCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
):
    # Проверка что проект существует и текущий пользователь - admin/owner
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    if project.workspace.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only workspace owner can add members"
        )

    # Проверка что пользователь не уже участник
    existing_member = db.query(ProjectMember).filter(
        ProjectMember.project_id == project_id,
        ProjectMember.user_id == member.user_id
    ).first()
    if existing_member:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is already a project member"
        )

    db_member = ProjectMember(**member.model_dump(), project_id=project_id)
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member


@router.get("/", response_model=list[ProjectMemberInDB])
def list_project_members(
        project_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
):
    # Проверка что пользователь имеет доступ к проекту
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    is_member = db.query(ProjectMember).filter(
        ProjectMember.project_id == project_id,
        ProjectMember.user_id == current_user.id
    ).first()

    if not is_member and project.workspace.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view project members"
        )

    members = db.query(ProjectMember).filter(ProjectMember.project_id == project_id).all()
    return members