import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.deps import get_db
from app.model import Base, User
from app.core.security import get_current_user # Import để ghi đè

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module")
def client():
    Base.metadata.create_all(bind=engine)
    
    def override_get_db():
        db = TestingSessionLocal()
        try: yield db
        finally: db.close()
    
    # GIẢI PHÁP: Giả lập người dùng luôn đăng nhập thành công cho bài test
    def override_get_current_user():
        return User(id=1, email="mtri20051002@gmail.com", is_active=True, role="admin")

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_get_current_user
    
    with TestClient(app) as c:
        yield c
    
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def normal_user_token_headers():
    return {"Authorization": "Bearer fake-token-for-test"}