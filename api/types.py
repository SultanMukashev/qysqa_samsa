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
    @classmethod
    def to_json(cls, user: User) -> dict:
        return cls(
            user_id=user.user_id,
            name=user.name,
            surname=user.surname,
        ).model_dump()
    


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
    name: str | None
    description: str | None
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
        content: str | None
        @classmethod
        def to_json(cls, lesson: Lesson) -> dict:
            return cls(
                lesson_id=lesson.lesson_id,
                name=lesson.title,
                content = lesson.conspect,
            ).model_dump()
    course_id: int
    name: str | None
    teacher: str | None
    description: str | None
    enrolled: bool
    lessons: list[LessonElement]

    @classmethod
    def to_json(cls, course: Course, enrolled: bool) -> dict:
        return cls(
            course_id=course.course_id,
            name=course.name,
            teacher=(course.teacher.name or '') + ' ' + (course.teacher.surname or '') if course.teacher else None,
            description=course.description,
            enrolled=enrolled,
            lessons=[cls.LessonElement.to_json(l) for l in course.lessons],
        ).model_dump()


class CreateLessonReq(BaseModel):
    title: str
    course_id: int

class CourseInfo(BaseModel):
    course_id: int
    name: str
    description: str
    @classmethod
    def to_json(cls, course: Course) -> dict:
        return cls(
            course_id=course.course_id,
            name=course.name,
            description=course.description,
        ).model_dump()

class LessonInfo(BaseModel):
    lesson_id: int
    title: str
    conspect: str | None
    content_file_url: str | None
    course: CourseInfo
    @classmethod
    def to_json(cls, lesson: Lesson) -> dict:
        return cls(
            lesson_id=lesson.lesson_id,
            title=lesson.title,
            conspect=lesson.conspect,
            content_file_url=lesson.content_file_url,
            course_id=lesson.course_id,
            course=CourseInfo.to_json(lesson.course),
        ).model_dump()


class LessonFullRes(BaseModel):
    lesson_id: int
    title: str
    conspect: str | None
    content_file_url: str | None
    course: CourseInfo

    @classmethod
    def to_json(cls, lesson: Lesson) -> dict:
        return cls(
            lesson_id=lesson.lesson_id,
            title=lesson.title,
            conspect=lesson.conspect,
            content_file_url=lesson.content_file_url,
            course=CourseInfo.to_json(lesson.course),
        ).model_dump()
class CourseMyRes(BaseModel):
    class LessonElement(BaseModel):
        lesson_id: int
        name: str
        content: str | None
        @classmethod
        def to_json(cls, lesson: Lesson) -> dict:
            return cls(
                lesson_id=lesson.lesson_id,
                name=lesson.title,
                content = lesson.conspect,
            ).model_dump()
    course_id: int
    name: str
    description: str
    lessons: list[LessonElement]

    @classmethod
    def to_json(cls, course: Course) -> dict:
        return cls(
            course_id=course.course_id,
            name=course.name,
            description=course.description,
            lessons=[cls.LessonElement.to_json(l) for l in course.lessons],
        ).model_dump()

class TeacherAuth(BaseModel):
    id: int
    password: str