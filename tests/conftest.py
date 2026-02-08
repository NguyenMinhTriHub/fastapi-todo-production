import sys
import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

# 1. FIX LỖI IMPORT: Thêm thư mục gốc vào PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Bây giờ mới có thể import main và database mà không bị lỗi
from app.main import app
from app.core.database import Base, get_db

# 2. CẤU HÌNH DATABASE THỬ NGHIỆM (SQLite cục bộ)
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    # Tạo cấu trúc bảng trong file test.db
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        # Xóa bảng sau khi test xong để đảm bảo sạch sẽ
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db_session):
    # Ghi đè (Override) database thật bằng database thử nghiệm
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    # Xóa cấu hình ghi đè sau khi test xong
    app.dependency_overrides.clear()