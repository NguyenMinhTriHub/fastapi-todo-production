from sqlalchemy.orm import Session
from app.models.todo_model import TodoModel # Sửa lại cho đúng tên file
from app.schemas.todo import TodoCreate

class TodoRepository:
    # Mở file app/repositories/todo_repo.py và cập nhật:

    def get_todos(self, db: Session, owner_id: int, skip: int = 0, limit: int = 10):
        # Thêm .filter(TodoModel.owner_id == owner_id)
        return db.query(TodoModel).filter(TodoModel.owner_id == owner_id).offset(skip).limit(limit).all()

    def get_total(self, db: Session, owner_id: int):
        # Đếm số lượng công việc của riêng User đó
        return db.query(TodoModel).filter(TodoModel.owner_id == owner_id).count()

    def create(self, db: Session, todo: TodoCreate, owner_id: int):
        # Gán owner_id cho bản ghi mới
        db_todo = TodoModel(**todo.model_dump(), owner_id=owner_id)
        db.add(db_todo)
        db.commit()
        db.refresh(db_todo)
        return db_todo

    def update_partial(self, db: Session, todo_id: int, todo_data: dict, owner_id: int):
        db.query(TodoModel).filter(TodoModel.id == todo_id, TodoModel.owner_id == owner_id).update(todo_data)
        db.commit()
        return db.query(TodoModel).filter(TodoModel.id == todo_id).first()