from app.repositories.todo_repo import TodoRepository
from app.schemas.todo import TodoCreate, TodoUpdate, TodoPaginationResponse
from sqlalchemy.orm import Session

class TodoService:
    def __init__(self):
        self.repo = TodoRepository()

# Cập nhật hàm list_todos để nhận thêm owner_id
# Mở file app/services/todo_service.py và cập nhật các hàm sau:

    def list_todos(self, db: Session, limit: int = 10, offset: int = 0, owner_id: int = None):
        # Nhận owner_id và truyền tiếp xuống Repository
        items = self.repo.get_todos(db, skip=offset, limit=limit, owner_id=owner_id) 
        total = self.repo.get_total(db, owner_id=owner_id)
        
        return TodoPaginationResponse(
            items=items,
            total=total,
            limit=limit,
            offset=offset
        )

    def create_todo(self, db: Session, todo: TodoCreate, owner_id: int):
        # Truyền owner_id khi tạo mới công việc
        return self.repo.create(db, todo, owner_id=owner_id)

    def partial_update(self, db: Session, todo_id: int, todo_in: TodoUpdate, owner_id: int):
        update_data = todo_in.model_dump(exclude_unset=True)
        # Đảm bảo chỉ cập nhật nếu đúng chủ sở hữu
        return self.repo.update_partial(db, todo_id, update_data, owner_id=owner_id)