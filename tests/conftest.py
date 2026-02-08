import pytest
import sys
import os
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Đảm bảo pytest tìm thấy thư mục app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.main import app
from app.deps import get_db, get_current_user
from app.model import Base, User, UserRole # Đảm bảo có UserRole ở đây

# Setup Database ảo cho môi trường test
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db_session):
    # Giả lập Admin để vượt qua lỗi 401/403
    def override_get_current_user():
        return User(id=1, email="test@example.com", role=UserRole.ADMIN)

    # Ghi đè Dependency
    app.dependency_overrides[get_db] = lambda: db_session
    app.dependency_overrides[get_current_user] = override_get_current_user
    
    with TestClient(app) as c:
        yield c
    
    app.dependency_overrides.clear()