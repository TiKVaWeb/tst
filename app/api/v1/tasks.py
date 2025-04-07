from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.project_member import ProjectMember
from app.models.user import User
from app.models.task import Task, TaskTag, Tag
from app.models.board import BoardColumn
from app.schemas.task import TaskCreate, TaskInDB, TaskUpdate, TagCreate, TagInDB
from app.database import get_db
from app.utils.security import get_current_active_user

router = APIRouter(prefix="/projects/{project_id}/tasks", tags=["tasks"])


@router.post("/", response_model=TaskInDB)
def create_task(
        project_id: int,
        task: TaskCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
):
    # Проверка доступа к проекту
    project_member = db.query(ProjectMember).filter(
        ProjectMember.project_id == project_id,
        ProjectMember.user_id == current_user.id
    ).first()

    if not project_member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create tasks in this project"
        )

    # Проверка что колонка существует в этом проекте
    column = db.query(BoardColumn).join(Board).filter(
        BoardColumn.id == task.column_id,
        Board.project_id == project_id
    ).first()

    if not column:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Column not found in this project"
        )

    # Создание задачи
    db_task = Task(
        **task.model_dump(exclude={"tag_ids"}),
        project_id=project_id,
        created_by=current_user.id
    )
    db.add(db_task)
    db.commit()

    # Добавление тегов
    if task.tag_ids:
        for tag_id in task.tag_ids:
            tag = db.query(Tag).filter(
                Tag.id == tag_id,
                Tag.project_id == project_id
            ).first()
            if tag:
                db_task_tag = TaskTag(task_id=db_task.id, tag_id=tag_id)
                db.add(db_task_tag)

    db.commit()
    db.refresh(db_task)
    return db_task


@router.put("/{task_id}", response_model=TaskInDB)
def update_task(
        project_id: int,
        task_id: int,
        task_update: TaskUpdate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
):
    # Логика обновления задачи с историей изменений
    pass