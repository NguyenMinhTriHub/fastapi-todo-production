import sys
import os

# Thêm thư mục hiện tại vào con đường tìm kiếm của Python để nhận diện thư mục 'app'
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import engine
from app import model

def create_tables():
    print("--- ĐANG KHỞI TẠO CƠ SỞ DỮ LIỆU TRÊN SUPABASE ---")
    try:
        # Lệnh quét toàn bộ các Model (User, Todo) và tạo bảng tương ứng
        model.Base.metadata.create_all(bind=engine)
        print("=> THÀNH CÔNG: Bảng 'users' và 'todos' đã được tạo với cột 'email'!")
    except Exception as e:
        print(f"=> THẤT BẠI: Không thể kết nối đến Supabase.")
        print(f"Lỗi chi tiết: {e}")

if __name__ == "__main__":
    create_tables()