from app.deps import engine
from app.model import Base, User
from app.core.security import get_password_hash
from sqlalchemy.orm import sessionmaker

def init_db():
    print("Đang đồng bộ cấu trúc bảng trên Supabase...")
    # Tạo bảng nếu chưa có
    Base.metadata.create_all(bind=engine)
    
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    user_email = "mtri20051002@gmail.com"
    # Bạn có thể đổi mật khẩu Admin tại đây
    admin_password = "AppDev2026a" 
    
    user = db.query(User).filter(User.email == user_email).first()
    if not user:
        print(f"Đang tạo tài khoản admin: {user_email}")
        admin_user = User(
            email=user_email,
            hashed_password=get_password_hash(admin_password),
            is_active=True,
            role="admin"
        )
        db.add(admin_user)
        db.commit()
    else:
        # Cập nhật mật khẩu mới nếu tài khoản đã tồn tại
        user.hashed_password = get_password_hash(admin_password)
        db.commit()
        print("Đã cập nhật mật khẩu cho tài khoản tồn tại.")
    
    db.close()
    print("Khởi tạo database thành công!")

if __name__ == "__main__":
    init_db()