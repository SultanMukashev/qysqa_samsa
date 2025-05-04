from pydantic import BaseModel
from typing import Optional

class CourseRes(BaseModel):
    course_id: int
    title: str
    description: Optional[str] = None

    @staticmethod
    def to_json(course):
        return {
            "course_id": course.course_id,
            "title": course.title,
            "description": course.description
        }

class CourseFullRes(CourseRes):
    lessons: list = []

    @staticmethod
    def to_json(course):
        base = CourseRes.to_json(course)
        base["lessons"] = [lesson.to_json() for lesson in course.lessons]
        return base 