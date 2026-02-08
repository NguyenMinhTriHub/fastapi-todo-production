from sqlalchemy.orm import Session
# Sử dụng dấu chấm để trỏ vào tệp model.py cùng cấp thư mục app
from app.model import Todo, UserRole, User

def list_all_todos(db: Session, limit: int, offset: int):
    return db.query(Todo).offset(offset).limit(limit).all()

def list_todos(db: Session, limit: int, offset: int, owner_id: int):
    return db.query(Todo).filter(Todo.owner_id == owner_id).offset(offset).limit(limit).all()

def partial_update(db: Session, todo_id: int, todo_in: dict, current_user: User):
    query = db.query(Todo).filter(Todo.id == todo_id)
    # Nếu không phải Admin thì chỉ được sửa đồ của mình
    if current_user.role != UserRole.ADMIN:
        query = query.filter(Todo.owner_id == current_user.id)
    
    db_todo = query.first()
    if db_todo:
        update_data = todo_in.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_todo, key, value)
        db.commit()
        db.refresh(db_todo)
    return db_todo