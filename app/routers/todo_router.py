from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import schemas, model, deps, crud
# Quan trọng: Gọi trực tiếp từ security để tránh lỗi Circular Import
from app.core.security import get_current_user 

router = APIRouter(prefix="/todos", tags=["todos"])

# API thêm công việc mới (Nút POST màu xanh lá)
@router.post("/", response_model=schemas.TodoResponse, status_code=status.HTTP_201_CREATED)
def create_todo(
    todo: schemas.TodoCreate, 
    db: Session = Depends(deps.get_db), 
    current_user: model.User = Depends(get_current_user)
):
    """
    Tạo một công việc mới cho người dùng hiện tại đã đăng nhập.
    """
    return crud.create_user_todo(db=db, todo=todo, user_id=current_user.id)

# API xem danh sách công việc (Nút GET màu xanh dương)
@router.get("/", response_model=list[schemas.TodoResponse])
def read_todos(
    skip: int = 0, 
    limit: int = 10, 
    db: Session = Depends(deps.get_db), 
    current_user: model.User = Depends(get_current_user)
):
    """
    Lấy danh sách các công việc thuộc sở hữu của người dùng hiện tại.
    """
    return crud.get_todos(db, skip=skip, limit=limit, user_id=current_user.id)