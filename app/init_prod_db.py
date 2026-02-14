from app.deps import engine
from app.model import Base, User
from app.core.security import get_password_hash
from sqlalchemy.orm import sessionmaker

def init_db():
    # Tạo cấu trúc bảng trên Supabase
    print("Đang tạo bảng trên Supabase...")
    Base.metadata.create_all(bind=engine)
    
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    # Kiểm tra và tạo User Admin nếu chưa có
    user_email = "mtri20051002@gmail.com"
    user = db.query(User).filter(User.email == user_email).first()
    
    if not user:
        print(f"Đang tạo tài khoản admin: {user_email}")
        admin_user = User(
            email=user_email,
            hashed_password=get_password_hash("AppDev2026a"), # Thay bằng mật khẩu của bạn
            is_active=True,
            role="admin"
        )
        db.add(admin_user)
        db.commit()
        print("Khởi tạo thành công!")
    else:
        print("Tài khoản đã tồn tại.")
    db.close()

if __name__ == "__main__":
    init_db()