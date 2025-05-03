from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from sqlalchemy.orm import Session
from utils.db import connect_db
from utils.auth import me_as_student
from utils.entities import User, Course, Enrollment
from .types import CourseRes, CourseFullRes, AuthReq, AuthRegReq, AuthRes

router = APIRouter(prefix="/students", tags=["students"])


@router.post('/auth', response_model=AuthRes)
def auth(req: AuthReq, db: Session = Depends(connect_db)):
    user = db.query(User).filter(User.student_id == req.student_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.password != req.password:
        raise HTTPException(status_code=401, detail="Invalid password")
    return AuthRes(user_id=user.user_id, name=user.name, surname=user.surname)


# @router.put('/auth', response_model=AuthRes)
# def auth(req: AuthRegReq, db: Session = Depends(connect_db)):
#     if db.query(User).filter(User.student_id == req.student_id).first():
#         raise HTTPException(status_code=400, detail="User exists")
#     user = User(student_id=req.student_id, password=req.password, name=req.name, surname=req.surname)
#     db.add(user)
#     db.commit()
#     db.refresh(user)
#     return AuthRes(user_id=user.user_id, name=user.name, surname=user.surname)


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