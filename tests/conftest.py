import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.deps import get_db
from app.model import Base
from app.core.security import create_access_token

# Sử dụng Database tạm thời để test
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module")
def client():
    Base.metadata.create_all(bind=engine)
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def normal_user_token_headers():
    """Tạo Token giả lập cho người dùng để test các API yêu cầu đăng nhập"""
    access_token = create_access_token(data={"sub": "mtri20051002@gmail.com"})
    return {"Authorization": f"Bearer {access_token}"}