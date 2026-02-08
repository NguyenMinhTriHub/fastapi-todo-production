import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# 1. Nạp các biến từ file .env vào hệ thống
load_dotenv()

# 2. Lấy URL kết nối database
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# 3. Cơ chế bảo vệ: Nếu biến môi trường bị trống (None), 
# tự động chuyển sang SQLite để bài test không bị sập
if SQLALCHEMY_DATABASE_URL is None:
    SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

# 4. Khởi tạo engine
# Thêm cấu hình check_same_thread nếu sử dụng SQLite
if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency cung cấp session database cho các API
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()