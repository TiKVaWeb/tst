from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.project import Project
from app.models.project_member import ProjectMember
from app.models.task import Task
from app.models.file import ProjectFile, TaskAttachment
from app.schemas.file import ProjectFileInDB, TaskAttachmentInDB
from app.database import get_db
from app.utils.security import get_current_active_user
from app.utils.file_storage import save_file, delete_file
import os

router = APIRouter(prefix="/projects/{project_id}/files", tags=["files"])


@router.post("/", response_model=ProjectFileInDB)
async def upload_file(
        project_id: int,
        file: UploadFile = File(...),
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
):
    # Проверка доступа к проекту
    is_member = db.query(ProjectMember).filter(
        ProjectMember.project_id == project_id,
        ProjectMember.user_id == current_user.id
    ).first()

    if not is_member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to upload files to this project"
        )

    # Сохранение файла
    file_path = await save_file(file, project_id)

    # Создание записи в БД
    db_file = ProjectFile(
        name=file.filename,
        path=file_path,
        project_id=project_id,
        uploaded_by=current_user.id,
        size=file.size,
        mime_type=file.content_type
    )
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file


@router.post("/tasks/{task_id}/attach", response_model=TaskAttachmentInDB)
async def attach_file_to_task(
        project_id: int,
        task_id: int,
        file_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
):
    # Проверка что файл и задача принадлежат проекту
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.project_id == project_id
    ).first()

    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    project_file = db.query(ProjectFile).filter(
        ProjectFile.id == file_id,
        ProjectFile.project_id == project_id
    ).first()

    if not project_file:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")

    # Проверка что пользователь имеет доступ к задаче
    is_member = db.query(ProjectMember).filter(
        ProjectMember.project_id == project_id,
        ProjectMember.user_id == current_user.id
    ).first()

    if not is_member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to attach files to this task"
        )

    # Проверка что файл еще не прикреплен
    existing_attachment = db.query(TaskAttachment).filter(
        TaskAttachment.task_id == task_id,
        TaskAttachment.file_id == file_id
    ).first()

    if existing_attachment:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File already attached to this task"
        )

    # Создание прикрепления
    attachment = TaskAttachment(
        task_id=task_id,
        file_id=file_id,
        uploaded_by=current_user.id
    )
    db.add(attachment)
    db.commit()
    db.refresh(attachment)
    return attachment