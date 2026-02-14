from fastapi import FastAPI
from app.routers import todo_router, auth_router
from app.model import Base
from app.deps import engine

# Tạo bảng tự động (nếu chưa có)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="To-do App Level 8")

app.include_router(auth_router.router)
app.include_router(todo_router.router)

@app.get("/")
def root():
    return {"message": "Server is running smoothly!"}