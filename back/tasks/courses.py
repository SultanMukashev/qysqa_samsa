# from celery import shared_task
from services.moodle import MoodleService
# from core.celery import celery_app
from db.database import Session

# @shared_task
def parse_course_task(course_id: int, user_id: int):
    # Инициализация сессии БД
    with Session() as db:
        moodle_service = MoodleService(db)
        # moodle_service.process_course_files(course_id, user_id)
