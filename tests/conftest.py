import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.deps import get_db
from app.model import Base, User
from app.core.security import create_access_token, get_password_hash

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module")
def client():
    # Tạo bảng và tạo user mẫu để test
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    if not db.query(User).filter(User.email == "mtri20051002@gmail.com").first():
        # Phải khớp hashed_password với model.py
        test_user = User(
            email="mtri20051002@gmail.com", 
            hashed_password=get_password_hash("testpass"), 
            is_active=True
        )
        db.add(test_user)
        db.commit()
    db.close()

    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()
            
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def normal_user_token_headers():
    access_token = create_access_token(data={"sub": "mtri20051002@gmail.com"})
    return {"Authorization": f"Bearer {access_token}"}