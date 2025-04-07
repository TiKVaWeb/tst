from sqlalchemy.orm import Session
from app.models.task_history import TaskHistory

def log_task_change(
    db: Session,
    task_id: int,
    user_id: int,
    change_type: str,
    old_value: str = None,
    new_value: str = None
):
    history = TaskHistory(
        task_id=task_id,
        changed_by=user_id,
        change_type=change_type,
        old_value=old_value,
        new_value=new_value
    )
    db.add(history)
    db.commit()