from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import schemas, model, deps, crud
# Quan trọng: Import trực tiếp từ core.security để tránh lỗi Circular Import
from app.core.security import get_current_user 

router = APIRouter(prefix="/todos", tags=["todos"])

# 1. API Tạo công việc mới (POST)
@router.post("/", response_model=schemas.TodoResponse, status_code=status.HTTP_201_CREATED)
def create_todo(
    todo: schemas.TodoCreate, 
    db: Session = Depends(deps.get_db), 
    current_user: model.User = Depends(get_current_user)
):
    """
    Tạo một Todo mới. Yêu cầu đăng nhập. 
    Dữ liệu sẽ được gắn với ID của người dùng đang truy cập.
    """
    return crud.create_user_todo(db=db, todo=todo, user_id=current_user.id)

# 2. API Lấy danh sách công việc (GET)
@router.get("/", response_model=list[schemas.TodoResponse])
def read_todos(
    skip: int = 0, 
    limit: int = 10, 
    db: Session = Depends(deps.get_db), 
    current_user: model.User = Depends(get_current_user)
):
    """
    Lấy danh sách Todo của người dùng hiện tại.
    Bắt buộc phải có current_user để tránh lỗi bảo mật (trả về 401 thay vì 200 khi chưa đăng nhập).
    """
    return crud.get_todos(db, skip=skip, limit=limit, user_id=current_user.id)