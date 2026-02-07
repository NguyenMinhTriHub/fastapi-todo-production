from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.todo import TodoCreate, TodoUpdate, TodoResponse, TodoPaginationResponse
from app.services.todo_service import TodoService
from app.models.user_model import UserModel

# IMPORT TỪ FILE DEPS BẠN VỪA TẠO
from app.routers.deps import get_current_user

router = APIRouter(prefix="/api/v1/todos", tags=["todos"])
service = TodoService()

@router.get("/", response_model=TodoPaginationResponse)
def read_todos(
    limit: int = 10,
    offset: int = 0,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user) # Bắt buộc có Token
):
    # Lọc dữ liệu theo owner_id để đảm bảo tính riêng tư
    return service.list_todos(db, limit, offset, owner_id=current_user.id)

@router.post("/", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
def create_todo(
    todo_in: TodoCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    # Gán chủ sở hữu khi tạo mới
    return service.create_todo(db, todo_in, owner_id=current_user.id)

@router.patch("/{todo_id}", response_model=TodoResponse)
def update_todo(
    todo_id: int,
    todo_in: TodoUpdate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    # Chỉ cho phép sửa nếu To-do đó thuộc sở hữu của current_user
    updated_item = service.partial_update(db, todo_id, todo_in, owner_id=current_user.id)
    if not updated_item:
        raise HTTPException(
            status_code=404, 
            detail="Không tìm thấy To-do hoặc bạn không có quyền truy cập"
        )
    return updated_item