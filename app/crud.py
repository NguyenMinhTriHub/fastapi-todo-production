from sqlalchemy.orm import Session
from app import model, schemas

# Hàm lấy danh sách công việc theo ID của người dùng
def get_todos(db: Session, skip: int = 0, limit: int = 10, user_id: int = None):
    return db.query(model.Todo).filter(model.Todo.owner_id == user_id).offset(skip).limit(limit).all()

# Hàm tạo công việc mới gắn với ID người dùng
def create_user_todo(db: Session, todo: schemas.TodoCreate, user_id: int):
    db_todo = model.Todo(**todo.model_dump(), owner_id=user_id)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo