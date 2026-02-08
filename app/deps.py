from fastapi import Depends, HTTPException, status
from typing import List
from app.model import User, UserRole # Import từ file model.py
from app.core.database import SessionLocal # Trỏ vào thư mục core
from app.core.security import get_current_user 

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class RoleChecker:
    def __init__(self, allowed_roles: List[UserRole]):
        self.allowed_roles = allowed_roles

    def __call__(self, user: User = Depends(get_current_user)):
        if user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Bạn không có quyền thực hiện hành động này"
            )
        return user

allow_admin_only = RoleChecker([UserRole.ADMIN])