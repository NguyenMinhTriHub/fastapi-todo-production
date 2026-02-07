from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Các biến cũ
    APP_NAME: str = "FastAPI Todo App"
    DEBUG: bool = True
    
    # KHAI BÁO THÊM CÁC BIẾN NÀY ĐỂ HẾT LỖI:
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    DATABASE_URL: str
    
    # Cấu hình để đọc file .env
    model_config = SettingsConfigDict(
        env_file=".env", 
        extra="ignore"  # THÊM DÒNG NÀY: Bỏ qua nếu có biến thừa trong .env
    )

settings = Settings()