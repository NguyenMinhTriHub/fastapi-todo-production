from fastapi import FastAPI, Response
from app.routers import todo_router  # Giả sử bạn đang dùng router này

app = FastAPI(title="FastAPI Todo Production")

# Endpoint xử lý favicon để tránh lỗi 404 trong logs
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    # Trả về mã 204 (No Content) để trình duyệt không báo lỗi
    return Response(status_code=204)

# Route gốc kiểm tra trạng thái ứng dụng
@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI Todo API - Production is Live!"}

# Đăng ký các router của bạn
app.include_router(todo_router.router, prefix="/api/v1")