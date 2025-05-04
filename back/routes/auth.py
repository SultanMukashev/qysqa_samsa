from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas.auth import AuthRequest
from services.auth import AuthService
from db.database import connect_db

router = APIRouter()

@router.post("/login")
async def login(
    auth_data: AuthRequest,
    db: Session = Depends(connect_db)
):
    auth_service = AuthService(db)
    user = await auth_service.authenticate(
        auth_data.username,
        auth_data.password
    )
    
    if not user:
        return {"error": "Invalid credentials"}
        
    return {
        "user_id": user.user_id,
        "courses": user.enrollments
    }
