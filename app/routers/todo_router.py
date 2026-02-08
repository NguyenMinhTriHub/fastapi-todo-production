from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app import schemas, model, deps
from app.services import todo_service as service

router = APIRouter(prefix="/todos", tags=["todos"])

@router.get("/", response_model=List[schemas.TodoResponse])
def read_todos(
    db: Session = Depends(deps.get_db),
    current_user: model.User = Depends(deps.get_current_user),
    limit: int = 10,
    offset: int = 0
):
    # Logic phân quyền Level 8
    if current_user.role == model.UserRole.ADMIN: # Đảm bảo model được nhận diện
        return service.list_all_todos(db, limit, offset)
    
    return service.list_todos(db, limit, offset, owner_id=current_user.id)