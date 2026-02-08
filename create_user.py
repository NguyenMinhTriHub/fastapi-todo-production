from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.model import User, UserRole
from app.core.security import get_password_hash # Đảm bảo file security.py có hàm này

def create_initial_user():
    db: Session = SessionLocal()
    email = "mtri20051002@gmail.com"
    password = "AppDev2026a" # Mật khẩu bạn muốn đặt

    # Kiểm tra xem user đã tồn tại chưa
    user = db.query(User).filter(User.email == email).first()
    if user:
        print(f"Người dùng {email} đã tồn tại!")
        return

    # Tạo user mới với mật khẩu đã được hash (mã hóa)
    hashed_password = get_password_hash(password)
    new_user = User(
        email=email,
        password=hashed_password,
        role=UserRole.ADMIN, # Gán luôn quyền Admin ở đây
        is_active=True
    )

    db.add(new_user)
    db.commit()
    print(f"--- THÀNH CÔNG: Đã tạo tài khoản Admin {email} ---")
    db.close()

if __name__ == "__main__":
    create_initial_user()