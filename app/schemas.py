from pydantic import BaseModel, EmailStr
from typing import Optional, List
from enum import Enum

# Định nghĩa lại Enum ở phía Pydantic để validate dữ liệu đầu vào
class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"

class UserBase(BaseModel):
    email: EmailStr
    role: Optional[UserRole] = UserRole.USER # Cho phép khai báo role khi tạo

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True