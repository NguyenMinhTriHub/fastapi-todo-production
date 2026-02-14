from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import schemas, model, deps, crud

router = APIRouter(prefix="/todos", tags=["todos"])

# Nút POST (Xanh lá) - Dùng để thêm công việc
@router.post("/", response_model=schemas.TodoResponse, status_code=status.HTTP_201_CREATED)
def create_todo(todo: schemas.TodoCreate, db: Session = Depends(deps.get_db), current_user: model.User = Depends(deps.get_current_user)):
    return crud.create_user_todo(db=db, todo=todo, user_id=current_user.id)

# Nút GET (Xanh dương) - Dùng để xem danh sách
@router.get("/", response_model=list[schemas.TodoResponse])
def read_todos(skip: int = 0, limit: int = 10, db: Session = Depends(deps.get_db), current_user: model.User = Depends(deps.get_current_user)):
    return crud.get_todos(db, skip=skip, limit=limit, user_id=current_user.id)