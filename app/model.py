import enum
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship
from .database import Base

# 1. Định nghĩa các vai trò cố định
class UserRole(str, enum.Enum):
    ADMIN = "admin"
    USER = "user"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    
    # 2. Thêm cột role với giá trị mặc định là 'user'
    role = Column(Enum(UserRole), default=UserRole.USER, nullable=False)

    todos = relationship("Todo", back_populates="owner")