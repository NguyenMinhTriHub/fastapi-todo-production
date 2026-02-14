from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# 1. Tạo Engine kết nối
engine = create_engine(settings.DATABASE_URL)

# 2. Tạo SessionLocal
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 3. Hàm lấy DB (Chỉ để lại hàm này)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()