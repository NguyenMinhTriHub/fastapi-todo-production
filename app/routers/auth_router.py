from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import deps, model
from app.core import security

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login")
def login_for_access_token(
    db: Session = Depends(deps.get_db), 
    form_data: OAuth2PasswordRequestForm = Depends()
):
    # 1. Tìm người dùng trong database theo email (username trong form)
    user = db.query(model.User).filter(model.User.email == form_data.username).first()
    
    # 2. Kiểm tra sự tồn tại của user và xác thực mật khẩu
    # SỬA LỖI TẠI ĐÂY: Sử dụng .hashed_password thay vì .password
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 3. Kiểm tra trạng thái hoạt động của tài khoản
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Inactive user"
        )
    
    # 4. Tạo mã Token truy cập (JWT)
    access_token = security.create_access_token(
        data={"sub": user.email}
    )
    
    return {"access_token": access_token, "token_type": "bearer"}