from pydantic import BaseModel
from utils.entities import Course, User, Lesson


class AuthReq(BaseModel):
    student_id: str
    password: str
class AuthRegReq(BaseModel):
    student_id: str
    password: str
    name: str
    surname: str
class AuthRes(BaseModel):
    user_id: int
    name: str
    surname: str


class UserRes(BaseModel):
    user_id: int
    first_name: str
    last_name: str
    student_id: int

    @classmethod
    def to_json(cls, user: User) -> dict:
        return cls(
            user_id=user.user_id,
            first_name=user.name,
            last_name=user.surname,
            student_id=user.student_id,
        ).model_dump()


class CourseRes(BaseModel):
    course_id: int
    name: str
    description: str
    lessons_count: int

    @classmethod
    def to_json(cls, course: Course) -> dict:
        return cls(
            course_id=course.course_id,
            name=course.name,
            description=course.description,
            lessons_count=len(course.lessons),
        ).model_dump()
class CourseFullRes(BaseModel):
    class LessonElement(BaseModel):
        lesson_id: int
        name: str
        @classmethod
        def to_json(cls, lesson: Lesson) -> dict:
            return cls(
                lesson_id=lesson.lesson_id,
                name=lesson.title,
            ).model_dump()
    course_id: int
    name: str
    description: str
    lessons: int

    @classmethod
    def to_json(cls, course: Course) -> dict:
        return cls(
            course_id=course.course_id,
            name=course.name,
            description=course.description,
            lessons=[cls.LessonElement.to_json(l) for l in course.lessons],
        ).model_dump()