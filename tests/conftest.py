import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.deps import get_db
from app.model import Base
# Quan trọng: Import từ app.core.security để tránh lỗi vòng lặp
from app.core.security import create_access_token 

# 1. Cấu hình Database giả lập (SQLite) để chạy test không ảnh hưởng database thật
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module")
def client():
    """Tạo một client giả lập để gửi các yêu cầu HTTP đến ứng dụng"""
    # Tạo cấu trúc bảng trong file test.db
    Base.metadata.create_all(bind=engine)
    
    # Ghi đè (Override) hàm get_db để ứng dụng dùng Database test thay vì Supabase
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()
            
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as c:
        yield c
    
    # Xóa dữ liệu sau khi test xong
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def normal_user_token_headers():
    """
    Tạo một 'chìa khóa' (Token) giả cho người dùng. 
    GitHub Actions sẽ dùng cái này để vượt qua lớp bảo mật Level 8.
    """
    access_token = create_access_token(data={"sub": "mtri20051002@gmail.com"})
    return {"Authorization": f"Bearer {access_token}"}