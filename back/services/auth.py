from sqlalchemy.orm import Session
from .moodle import MoodleService
from db.models import User, Enrollment, Course
from schemas.auth import UserCreate

class AuthService:
    def __init__(self, db: Session):
        self.db = db
        
    async def authenticate(self, username: str, password: str):
        user = self.db.query(User).filter(
            User.student_id == username,
            User.password == password
        ).first()
        
        if not user:
            # Moodle auth fallback
            moodle_service = MoodleService(username=username, password=password)
            moodle_user = await moodle_service.login()
            if not moodle_user:
                return None
                
            # Create new user
            user = User(
                student_id=username,
                password=password,
                name=moodle_user['first_name'],
                surname=moodle_user['last_name']
            )
            self.db.add(user)
            self.db.commit()
            
            # Enroll courses and trigger parsing
            await self._process_moodle_courses(user, username, password)
            
        return user
        
    async def _process_moodle_courses(self, user: User, username: str, password: str):
        # Get courses from Moodle
        moodle_service = MoodleService(username=username, password=password)
        courses = await moodle_service.get_courses()
        
        for course in courses:
            # Check if course exists
            db_course = self.db.query(Course).filter(
                Course.course_id == course['course_id']
            ).first()
            
            if not db_course:
                db_course = Course(
                    course_id=course['course_id'],
                    name=course['full_title']
                )
                self.db.add(db_course)
                
            # Create enrollment
            enrollment = Enrollment(
                user_id=user.user_id,
                course_id=db_course.course_id
            )
            self.db.merge(enrollment)
            
            # Trigger course parsing if no lessons
            # if not db_course.lessons:
            #     from tasks.courses import parse_course_task
            #     parse_course_task.delay(
            #         course_id=db_course.course_id,
            #         user_id=user.user_id,
            #         username=username,
            #         password=password
            #     )
        
        self.db.commit()

    async def get_user_courses(self, user_id: int, username: str, password: str):
        # First check if user exists
        user = self.db.query(User).filter(User.user_id == user_id).first()
        
        if not user:
            # If user doesn't exist, try to authenticate with Moodle
            moodle_service = MoodleService(username=username, password=password)
            moodle_user = await moodle_service.login()
            if not moodle_user:
                return None
                
            # Create new user
            user = User(
                student_id=username,
                password=password,
                name=moodle_user['first_name'],
                surname=moodle_user['last_name']
            )
            self.db.add(user)
            self.db.commit()
            
            # Get courses from Moodle
            courses = await moodle_service.get_courses()
            
            # Process courses for the new user
            await self._process_moodle_courses(user, username, password)
        else:
            # If user exists, just get their courses from Moodle
            moodle_service = MoodleService(username=user.student_id, password=user.password)
            courses = await moodle_service.get_courses()
        
        return {
            "user_id": user.user_id,
            "username": user.student_id,
            "courses": [
                {
                    "course_id": course["course_id"],
                    "title": course["full_title"],
                    "user_id": user.user_id
                }
                for course in courses
            ]
        }