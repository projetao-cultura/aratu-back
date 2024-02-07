from pydantic import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Aratu API"
    DEBUG_MODE: bool = True
    DATABASE_URL: str = "sqlite+aiosqlite:///./test.db"

    class Config:
        env_file = ".env"


settings = Settings()