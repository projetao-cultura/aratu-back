from pydantic import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "My FastAPI App"
    DEBUG_MODE: bool = True
    DATABASE_URL: str = "sqlite:///./test.db"

    class Config:
        env_file = ".env"


settings = Settings()