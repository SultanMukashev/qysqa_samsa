# app/core/celery.py
from celery import Celery
from core.config import settings
from db.database import SessionLocal

celery = Celery(
    "worker",
    broker=settings.CELERY_BROKER,
    backend=settings.CELERY_BACKEND,
    include=["app.tasks.courses"]
)

# Конфигурация
celery.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Almaty",
    enable_utc=True,
    task_track_started=True,
    result_extended=True,
    worker_max_tasks_per_child=100,
    broker_connection_retry_on_startup=True,
)

# Инициализация сессии БД для задач
@celery.task_postrun.connect
def close_session(*args, **kwargs):
    db = SessionLocal()
    try:
        db.close()
    except Exception as e:
        print(f"Error closing DB session: {e}")

# Периодические задачи (пример)
celery.conf.beat_schedule = {
    "cleanup-tasks-every-hour": {
        "task": "app.tasks.maintenance.cleanup_old_tasks",
        "schedule": 3600,  # каждые 60 минут
    },
}

if __name__ == "__main__":
    celery.start()