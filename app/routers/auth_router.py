from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import create_access_token, get_password_hash, verify_password
from app.models.user_model import UserModel
from app.schemas.user import UserCreate, UserResponse, Token

router = APIRouter(prefix="/api/v1/auth", tags=["auth"]) # Sử dụng tiền tố v1 đồng bộ

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    # 1. Kiểm tra xem username đã tồn tại chưa
    user_exists = db.query(UserModel).filter(UserModel.username == user_in.username).first()
    if user_exists:
        raise HTTPException(status_code=400, detail="Tên đăng nhập đã tồn tại")
    
    # 2. Băm mật khẩu và lưu vào Database
    hashed_pwd = get_password_hash(user_in.password)
    new_user = UserModel(username=user_in.username, hashed_password=hashed_pwd)
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # 1. Tìm người dùng theo username
    user = db.query(UserModel).filter(UserModel.username == form_data.username).first()
    
    # 2. Kiểm tra tài khoản và mật khẩu
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Tên đăng nhập hoặc mật khẩu không chính xác",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 3. Tạo JWT Token trả về cho người dùng
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}