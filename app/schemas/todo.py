from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class TodoBase(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=100)
    description: Optional[str] = None
    is_done: Optional[bool] = False

class TodoCreate(TodoBase):
    title: str = Field(..., min_length=3, max_length=100)

class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_done: Optional[bool] = None

class TodoResponse(TodoBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True # Quan trọng: Giúp chuyển đổi từ ORM sang JSON

class TodoPaginationResponse(BaseModel): # Sửa lỗi ImportError
    items: List[TodoResponse]
    total: int
    limit: int
    offset: int