from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from app.core.config import settings

# 1. Lấy URL kết nối từ settings (đã được nạp từ file .env)
# Nếu không tìm thấy, mặc định quay về SQLite để tránh lỗi crash
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./sql_app.db")

# 2. Cấu hình Engine
# Lưu ý: 'check_same_thread' chỉ cần thiết cho SQLite. 
# Khi dùng PostgreSQL, ta cần loại bỏ tham số này.
if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(SQLALCHEMY_DATABASE_URL)

# 3. Tạo SessionLocal để quản lý các phiên làm việc với DB
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Định nghĩa Base class để các Models kế thừa
Base = declarative_base()

# 5. Dependency: Hàm cung cấp session cho các Router
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()