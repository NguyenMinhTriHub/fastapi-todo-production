from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import schemas, model, deps # Sử dụng deps.py tập trung
from app.services import todo_service as service

router = APIRouter(prefix="/todos", tags=["todos"])

@router.get("/", response_model=List[schemas.TodoResponse])
def read_todos(
    db: Session = Depends(deps.get_db),
    current_user: model.User = Depends(deps.get_current_user),
    limit: int = 10,
    offset: int = 0
):
    # ADMIN: Lấy tất cả To-do của hệ thống
    if current_user.role == model.UserRole.ADMIN:
        return service.list_all_todos(db, limit, offset)
    
    # USER: Chỉ lấy To-do của chính mình
    return service.list_todos(db, limit, offset, owner_id=current_user.id)

@router.patch("/{todo_id}", response_model=schemas.TodoResponse)
def update_todo(
    todo_id: int,
    todo_in: schemas.TodoUpdate,
    db: Session = Depends(deps.get_db),
    current_user: model.User = Depends(deps.get_current_user)
):
    # Cho phép Admin sửa bất kỳ To-do nào, hoặc User sửa đồ của chính mình
    updated_item = service.partial_update(
        db, 
        todo_id=todo_id, 
        todo_in=todo_in, 
        current_user=current_user
    )
    if not updated_item:
        raise HTTPException(
            status_code=404, 
            detail="Không tìm thấy To-do hoặc bạn không có quyền truy cập"
        )
    return updated_item