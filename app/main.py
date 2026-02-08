from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.core.database import engine, get_db, Base
from app.models import todo_model

# Tạo bảng tự động khi khởi động (Cần thiết cho bài test)
todo_model.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Bản Level 7 đã sẵn sàng để xanh hóa!"}

# Thêm ít nhất một endpoint mẫu có dùng DB để pass qua bài test
@app.get("/todos")
def read_todos(db: Session = Depends(get_db)):
    return db.query(todo_model.Todo).all()