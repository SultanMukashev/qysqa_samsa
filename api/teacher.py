from fastapi import APIRouter, HTTPException, Depends, UploadFile
from io import BytesIO
from sqlalchemy.orm import Session
from utils.db import connect_db
from utils.auth import me_as_teacher
from utils.entities import User, Course, Enrollment, Lesson
from utils.s3 import S3FileProcessor, TextSummarizer
from .types import CreateLessonReq, LessonInfo, CourseRes, CourseMyRes, TeacherAuth, AuthRes

router = APIRouter(prefix="/teachers", tags=["teachers"])


@router.post('/auth', response_model=AuthRes)
def auth_teacher(req: TeacherAuth, db: Session = Depends(connect_db)):
    user = db.query(User).filter(User.user_id == req.id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.password != req.password:
        raise HTTPException(status_code=403, detail="Invalid password")
    return AuthRes.to_json(user)

@router.get('/am', response_model=bool)
def am_i_teacher(me: User = Depends(me_as_teacher)):
    return True


@router.get('/courses/my', response_model=list[CourseRes])
def get_my_courses(me: User = Depends(me_as_teacher), db: Session = Depends(connect_db)):
    courses = db.query(Course).filter(Course.teacher_id == me.user_id).all()
    return [CourseRes.to_json(c) for c in courses]

@router.get('/courses/my/{course_id}', response_model=CourseMyRes)
def get_my_course(course_id: int, me: User = Depends(me_as_teacher), db: Session = Depends(connect_db)):
    course = db.query(Course).filter(Course.course_id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    if course.teacher_id != me.user_id:
        raise HTTPException(status_code=403, detail="Forbidden")
    return CourseMyRes.to_json(course)


@router.post('/lessons', response_model=LessonInfo)
def create_lesson(req: CreateLessonReq, me: User = Depends(me_as_teacher), db: Session = Depends(connect_db)):
    course = db.query(Course).filter(Course.course_id == req.course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    if course.teacher_id != me.user_id:
        print(course.teacher_id, me.user_id)
        raise HTTPException(status_code=403, detail="Forbidden")
    lesson = Lesson(title=req.title, course_id=req.course_id)
    db.add(lesson)
    db.commit()
    db.refresh(lesson)
    return LessonInfo.to_json(lesson)


@router.post('/lessons/{lesson_id}/upload', response_model=LessonInfo)
def upload_lesson(lesson_id: int, file: UploadFile, me: User = Depends(me_as_teacher), db: Session = Depends(connect_db)):
    lesson = db.query(Lesson).filter(Lesson.lesson_id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    if lesson.course.teacher_id != me.user_id:
        raise HTTPException(status_code=403, detail="Forbidden")

    key = f'lessons/{lesson_id}/{file.filename}'
    s3 = S3FileProcessor('contents')
    try:
        link = s3.upload_file(BytesIO(file.file.read()), key)
        text = s3.get_file_text(key)
        conspect = TextSummarizer().summarize(text)
        lesson.content_file_url = link
        lesson.conspect = conspect
        db.add(lesson)
        db.commit()
        db.refresh(lesson)
    except:
        db.rollback()
        raise HTTPException(status_code=500, detail="File upload failed")
    return LessonInfo.to_json(lesson)