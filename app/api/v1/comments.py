from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.task import Task
from app.models.user import User
from app.models.project_member import ProjectMember
from app.models.comment import Comment
from app.schemas.comment import CommentCreate, CommentInDB
from app.database import get_db
from app.utils.security import get_current_active_user

router = APIRouter(prefix="/tasks/{task_id}/comments", tags=["comments"])


@router.post("/", response_model=CommentInDB)
def create_comment(
        task_id: int,
        comment: CommentCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
):
    # Проверка доступа к задаче
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    is_member = db.query(ProjectMember).filter(
        ProjectMember.project_id == task.project_id,
        ProjectMember.user_id == current_user.id
    ).first()

    if not is_member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to comment on this task"
        )

    db_comment = Comment(
        content=comment.content,
        task_id=task_id,
        user_id=current_user.id
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment