from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.board import Board, BoardColumn
from app.models.user import User
from app.models.project import Project
from app.models.project_member import ProjectMember
from app.schemas.board import BoardCreate, BoardInDB, BoardUpdate, BoardColumnCreate
from app.database import get_db
from app.utils.security import get_current_active_user

router = APIRouter(prefix="/projects/{project_id}/boards", tags=["boards"])


@router.post("/", response_model=BoardInDB)
def create_board(
        project_id: int,
        board: BoardCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
):
    # Проверка доступа к проекту
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
            detail="Not authorized to create boards in this project"
        )

    # Создание доски
    db_board = Board(
        name=board.name,
        project_id=project_id,
        created_by=current_user.id
    )
    db.add(db_board)
    db.commit()
    db.refresh(db_board)

    # Создание колонок
    for idx, column in enumerate(board.columns):
        db_column = BoardColumn(
            name=column.name,
            board_id=db_board.id,
            position=idx
        )
        db.add(db_column)

    db.commit()
    db.refresh(db_board)
    return db_board