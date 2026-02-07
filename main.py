from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="Todo App - Level 4 (In-memory)")

# 1. Định nghĩa Schema bằng Pydantic
class Todo(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False

# 2. Khởi tạo danh sách lưu trữ tạm thời (Thay thế cho Database)
todos = []

# 3. Các Endpoint xử lý dữ liệu
@app.get("/", tags=["Root"])
def home():
    return {"status": "success", "message": "Ứng dụng Level 4 đang chạy mượt mà!"}

@app.get("/todos", response_model=List[Todo])
def read_all_todos():
    return todos

@app.post("/todos", response_model=Todo)
def add_todo(todo: Todo):
    # Kiểm tra trùng ID
    if any(item.id == todo.id for item in todos):
        raise HTTPException(status_code=400, detail="ID này đã tồn tại trong danh sách")
    todos.append(todo)
    return todo

@app.delete("/todos/{todo_id}")
def remove_todo(todo_id: int):
    global todos
    initial_length = len(todos)
    todos = [item for item in todos if item.id != todo_id]
    if len(todos) == initial_length:
        raise HTTPException(status_code=404, detail="Không tìm thấy ID để xóa")
    return {"message": f"Đã xóa thành công Todo ID {todo_id}"}