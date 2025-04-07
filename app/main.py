from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import engine
from app.models import (
    user, workspace, project, project_member,
    board, board_column, task, tag, task_tag,
    comment, project_file, task_attachment, task_history
)
from app.api.v1 import api_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Jira-like Project Management API",
    version="1.0.0",
    contact={
        "name": "Your Name",
        "email": "your.email@example.com",
    },
    license_info={
        "name": "MIT",
    },
)

# Настройка CORS
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Включение роутеров API
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.on_event("startup")
async def startup():
    # Можно добавить логику инициализации при запуске
    pass

@app.on_event("shutdown")
async def shutdown():
    # Можно добавить логику при завершении работы
    pass

@app.get("/")
def read_root():
    return {
        "message": "Project Management API",
        "version": app.version,
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health")
def health_check():
    return {"status": "ok"}

# Для автоматического создания таблиц (лучше использовать Alembic для продакшена)
if settings.ENVIRONMENT == "dev":
    @app.on_event("startup")
    async def init_db():
        async with engine.begin() as conn:
            # await conn.run_sync(Base.metadata.drop_all)  # Раскомментировать для сброса БД
            await conn.run_sync(Base.metadata.create_all)