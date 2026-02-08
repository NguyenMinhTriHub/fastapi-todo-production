from pydantic import BaseModel, ConfigDict
from typing import Optional

class TodoBase(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False

# Lớp bị thiếu khiến Pytest báo lỗi
class TodoCreate(TodoBase):
    pass

class TodoResponse(TodoBase):
    id: int
    owner_id: int
    model_config = ConfigDict(from_attributes=True)