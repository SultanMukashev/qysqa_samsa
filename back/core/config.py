from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    AWS_BUCKET: str
    AWS_KEY: str 
    AWS_SECRET: str
    MOODLE_TIMEOUT: int = 30
    JWT_SECRET: str
    
    # Celery settings
    CELERY_BROKER: str = "sqla+sqlite:///celery.sqlite"
    CELERY_BACKEND: str = "db+sqlite:///celery.sqlite"
    CELERY_RESULT_EXPIRES: int = 3600  # 1 hour
    CELERY_TASK_SERIALIZER: str = "json"
    CELERY_RESULT_SERIALIZER: str = "json"
    CELERY_ACCEPT_CONTENT: list = ["json"]
    CELERY_TIMEZONE: str = "UTC"

    class Config:
        env_file = ".env"

settings = Settings()