from fastapi import FastAPI
from app.routers import todo_router, auth_router # Thêm auth_router vào đây
from app.core.config import settings
from app.core.database import engine, Base

# --- KHỞI TẠO DATABASE (Cấp độ 4 & 5) ---
# Tự động tạo bảng 'users' và cập nhật bảng 'todos' với trường 'owner_id'
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG
)

# --- ĐĂNG KÝ ROUTER ---
# Router xác thực (Mới bổ sung cho Cấp độ 5)
app.include_router(auth_router.router)

# Router quản lý công việc (Đã có từ Cấp độ 3)
app.include_router(todo_router.router)

# --- ENDPOINT CƠ BẢN ---
@app.get("/")
def read_root():
    return {"message": f"Chào mừng bạn đến với {settings.APP_NAME}!"}

@app.get("/health")
def health_check():
    return {"status": "ok"}