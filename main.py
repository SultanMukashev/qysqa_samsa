from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from utils.entities import BaseEntity
from utils.db import engine
from api.main import router as main_router
from api.student import router as student_router
from api.teacher import router as teacher_router

BaseEntity.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins = ['*'],
    allow_credentials = True,
    allow_methods = ['*'],
    allow_headers = ['*'],
    expose_headers = ['*'],
)

app.include_router(main_router)
app.include_router(student_router)
app.include_router(teacher_router)