from pydantic import BaseModel

class AuthRequest(BaseModel):
    username: str
    password: str

class UserCreate(BaseModel):
    student_id: str
    password: str
    name: str
    surname: str