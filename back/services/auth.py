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
            moodle_user = await MoodleService().login(username, password)
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
            await self._process_moodle_courses(user)
            
        return user
        
    async def _process_moodle_courses(self, user: User):
        # Get courses from Moodle
        courses = await MoodleService().get_courses(user.student_id, user.password)
        
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
            if not db_course.lessons:
                from tasks.courses import parse_course_task
                parse_course_task.delay(
                    course_id=db_course.course_id,
                    user_id=user.user_id
                )
        
        self.db.commit()