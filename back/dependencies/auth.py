from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.database import connect_db
from db.models import User

async def me_as_student(db: Session = Depends(connect_db)) -> User:
    # TODO: Implement actual user authentication
    user = db.query(User).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    return user 