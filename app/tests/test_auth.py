import pytest

# 1. Test đăng ký thành công
def test_register_user_success(client):
    response = client.post(
        "/api/v1/auth/register",
        json={"username": "testuser", "password": "password123"}
    )
    assert response.status_code == 201
    assert response.json()["username"] == "testuser"

# 2. Test lỗi 422 khi thiếu dữ liệu đăng ký
def test_register_user_missing_field(client):
    response = client.post(
        "/api/v1/auth/register",
        json={"username": "testuser"} # Thiếu password
    )
    assert response.status_code == 422
    assert "detail" in response.json()

# 3. Test đăng nhập thành công (Dùng Form-data)
def test_login_success(client):
    # Bước 1: Tạo user trước
    client.post("/api/v1/auth/register", json={"username": "tri_nguyen", "password": "password123"})
    
    # Bước 2: Đăng nhập bằng Form-data
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "tri_nguyen", "password": "password123"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

# 4. Test lỗi 401 khi sai mật khẩu
def test_login_wrong_password(client):
    client.post("/api/v1/auth/register", json={"username": "tri_nguyen", "password": "password123"})
    
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "tri_nguyen", "password": "wrongpassword"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Tên đăng nhập hoặc mật khẩu không chính xác"