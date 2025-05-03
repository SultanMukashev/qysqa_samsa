from jose import JWTError, jwt
from datetime import datetime, timedelta, UTC
from core.config import settings

def create_access_token(data: dict) -> str:
    expires = datetime.now(UTC) + timedelta(hours=24)
    return jwt.encode(
        {**data, "exp": expires}, 
        settings.JWT_SECRET,
        algorithm="HS256"
    )

