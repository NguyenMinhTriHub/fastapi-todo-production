from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from app.model import UserRole

# --- SCHEMA CHO NGƯỜI DÙNG (USERS) ---
class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool
    role: UserRole # Đảm bảo sử dụng Enum UserRole từ model

    # Cập nhật model_config để tương thích Pydantic V2 (Xóa cảnh báo vàng)
    model_config = ConfigDict(from_attributes=True)

# --- SCHEMA CHO XÁC THỰC (AUTHENTICATION) ---
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    # Đảm bảo tên lớp là TokenData (không có chữ 'p' thừa ở cuối)
    email: Optional[str] = None