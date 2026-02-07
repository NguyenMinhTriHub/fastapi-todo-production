from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey # Thêm ForeignKey
from sqlalchemy.orm import relationship # Thêm relationship
from sqlalchemy.sql import func
from app.core.database import Base
class TodoModel(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    is_done = Column(Boolean, default=False)
    
    # Tiêu chí Cấp 4: Tự động ghi nhận thời gian
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("UserModel", back_populates="todos")