from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    DATABASE_URL: str = "" 
    SECRET_KEY: str = "your_secret_key_here"
    ALGORITHM: str = "HS256"

    POSTGRES_USER: Optional[str] = None
    POSTGRES_PASSWORD: Optional[str] = None
    POSTGRES_DB: Optional[str] = None
    POSTGRES_HOST: Optional[str] = None
    POSTGRES_PORT: Optional[str] = "5432"

    # Cấu hình Pydantic V2 chuẩn
    model_config = SettingsConfigDict(env_file=".env", extra='ignore')

settings = Settings()