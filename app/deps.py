from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
# Thêm dòng này để nạp hàm xác thực người dùng
from app.core.security import get_current_user 

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()