from fastapi import Depends, HTTPException, status
from typing import List
from app.model import User, UserRole
from app.database import SessionLocal
from app.core.security import get_current_user # Giả định hàm này lấy user từ JWT

# Dependency lấy Database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Class kiểm tra quyền hạn (Role Checker)
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

# Các bộ lọc quyền sẵn có
allow_admin_only = RoleChecker([UserRole.ADMIN])