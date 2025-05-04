from fastapi import HTTPException, status, Depends, Header
from sqlalchemy.orm import Session
from .entities import User
from .db import connect_db


def auth_me(id: int = Header(alias = 'auth'), db: Session = Depends(connect_db)) -> User:
    if not id: raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Unauthorized")
    user = db.query(User).filter(User.user_id == id).first()
    if not user: raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Unauthorized")
    return user


def me_as_student(me: User = Depends(auth_me)) -> User:
    if me.student_id is None: raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "Forbidden")
    return me


def me_as_teacher(me: User = Depends(auth_me)) -> User:
    if me.student_id is not None: raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "Forbidden")
    return me