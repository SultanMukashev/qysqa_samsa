from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.auth import AuthRequest
from services.auth import AuthService
from db.database import connect_db
from db.models import Course, Enrollment, User
from schemas.course import CourseRes, CourseFullRes
from dependencies.auth import me_as_student


router = APIRouter()

@router.get('/courses', response_model=List[CourseRes])
def get_courses(me: User = Depends(me_as_student), db: Session = Depends(connect_db)):
    courses = db.query(Course).filter(Enrollment.user_id == me.user_id).all()
    return [CourseRes.to_json(course) for course in courses]


@router.get('/courses/{course_id}')
def get_course(course_id: int, me: User = Depends(me_as_student), db: Session = Depends(connect_db)):
    course = db.query(Course).filter(Course.course_id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return CourseFullRes.to_json(course)


@router.post('/courses/{course_id}')
def enrol(course_id: int, me: User = Depends(me_as_student), db: Session = Depends(connect_db)):
    course = db.query(Course).filter(Course.course_id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    if db.query(Enrollment).filter(Enrollment.user_id == me.user_id, Enrollment.course_id == course_id).first():
        raise HTTPException(status_code=400, detail="Already enrolled in this course")

    enrollment = Enrollment(user_id=me.user_id, course_id=course_id)
    db.add(enrollment)
    db.commit()
    return {"message": "Enrolled successfully"}