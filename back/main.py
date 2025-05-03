from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from utils.entities import BaseEntity
from utils.db import engine
from api.student import router as student_router

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

app.include_router(student_router)