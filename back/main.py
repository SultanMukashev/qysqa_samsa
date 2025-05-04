# app/main.py
from fastapi import FastAPI, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from sqlalchemy.orm import Session
from sqlalchemy import text
import uvicorn

from core.config import settings
from db.database import engine, Base, connect_db
from routes import auth, courses

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Инициализация БД при старте
    Base.metadata.create_all(bind=engine)
    
    # Проверка подключения к БД
    with Session(engine) as session:
        session.execute(text("SELECT 1"))
        print("✅ Database connection established")
    
    yield
    
    # Очистка при завершении
    print("⏹️ Shutting down application")

app = FastAPI(
    title="Moodle Integration API",
    description="API for integrating Moodle LMS with custom platform",
    version="1.0.0",
    lifespan=lifespan
)

# CORS Настройки
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение роутов
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(courses.router, prefix="/courses", tags=["Courses"])

@app.get("/", status_code=status.HTTP_200_OK)
async def root():
    return {
        "message": "Moodle Integration Service",
        "documentation": "/docs",
        "status": "operational"
    }

# Для запуска вручную
if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG
    )