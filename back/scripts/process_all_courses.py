import sys
from pathlib import Path

# Добавляем корневую директорию проекта в PYTHONPATH
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

import asyncio
from services.moodle import MoodleService
from db.database import Session, engine
from db.models import User, Enrollment


# Инициализация базы данных

async def process_all_courses():
    with Session() as db:
        try:
            # Получаем все enrollment с course_id > 1000
            enrollments = db.query(Enrollment).filter(Enrollment.course_id > 1000).all()
            
            if not enrollments:
                print("No enrollments found with course_id > 1000")
                return
            
            # Создаем словарь для группировки курсов по пользователям
            user_courses = {}
            for enrollment in enrollments:
                if enrollment.user_id not in user_courses:
                    user_courses[enrollment.user_id] = []
                user_courses[enrollment.user_id].append(enrollment.course_id)
            
            # Обрабатываем курсы для каждого пользователя
            for user_id, course_ids in user_courses.items():
                user = db.query(User).filter(User.user_id == user_id).first()
                if not user:
                    print(f"User {user_id} not found")
                    continue
                    
                print(f"Processing courses for user {user.student_id}")
                
                # Создаем сервис Moodle для пользователя
                moodle_service = MoodleService(
                    username=user.student_id,
                    password=user.password
                )
                
                for course_id in course_ids:
                    try:
                        print(f"Processing course {course_id} for user {user.student_id}")
                        await moodle_service.process_course_files(
                            course_id=course_id,
                            user_id=user.user_id
                        )
                        print(f"Successfully processed course {course_id}")
                    except Exception as e:
                        print(f"Error processing course {course_id}: {str(e)}")
                        continue
        except Exception as e:
            print(f"Database error: {str(e)}")
            raise

if __name__ == "__main__":
    asyncio.run(process_all_courses()) 