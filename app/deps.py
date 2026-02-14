from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# 1. Tạo bộ máy kết nối (Engine) - Đây là thứ đang bị thiếu!
engine = create_engine(settings.DATABASE_URL)

# 2. Tạo phiên làm việc (Session)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 3. Hàm hỗ trợ lấy DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()