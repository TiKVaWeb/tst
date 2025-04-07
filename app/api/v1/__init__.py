from fastapi import APIRouter
from app.api.v1 import (
    users,
    workspaces,
    projects,
    project_members,
    boards,
    tasks,
    comments,
    files,
)

router = APIRouter()
router.include_router(users.router, prefix="/users", tags=["users"])
router.include_router(workspaces.router, prefix="/workspaces", tags=["workspaces"])
router.include_router(projects.router, prefix="/projects", tags=["projects"])
router.include_router(project_members.router, tags=["project_members"])
router.include_router(boards.router, tags=["boards"])
router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
router.include_router(comments.router, tags=["comments"])
router.include_router(files.router, tags=["files"])