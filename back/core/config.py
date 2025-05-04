from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    AWS_BUCKET: str
    AWS_KEY: str 
    AWS_SECRET: str
    MOODLE_TIMEOUT: int = 30
    JWT_SECRET: str
    CELERY_BROKER: str = "redis://localhost:6379"

    class Config:
        env_file = ".env"

settings = Settings()