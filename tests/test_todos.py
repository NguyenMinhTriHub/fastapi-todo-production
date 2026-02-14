import pytest

def test_read_main(client):
    """Kiểm tra xem API trang chủ có hoạt động không"""
    response = client.get("/")
    assert response.status_code == 200
    # Lưu ý: Message phải khớp chính xác với file app/main.py của bạn
    assert response.json() == {"message": "Server is running smoothly!"}

def test_get_todos_unauthorized(client):
    """Kiểm tra: Nếu không đăng nhập thì không được xem danh sách Todo"""
    response = client.get("/todos/")
    # Level 8 yêu cầu token, nên nếu không có sẽ trả về 401
    assert response.status_code == 401

def test_get_todos_empty(client, normal_user_token_headers):
    """Kiểm tra danh sách Todo ban đầu của người dùng phải trống"""
    response = client.get("/todos/", headers=normal_user_token_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 0

def test_create_todo(client, normal_user_token_headers):
    """Kiểm tra tính năng thêm công việc mới (POST)"""
    new_todo = {
        "title": "Test Todo GitHub",
        "description": "Kiểm tra tính năng tự động trên GitHub Actions",
        "completed": False
    }
    response = client.post(
        "/todos/", 
        json=new_todo, 
        headers=normal_user_token_headers
    )
    assert response.status_code == 201
    assert response.json()["title"] == new_todo["title"]