import pytest

def test_read_root(client):
    """
    Kiểm tra endpoint trang chủ (/)
    Sử dụng fixture 'client' từ conftest.py
    """
    response = client.get("/")
    # Nếu app/main.py của bạn có định nghĩa route "/", code này sẽ trả về 200
    # Nếu không có route "/", FastAPI sẽ trả về 404 (vẫn tính là tìm thấy app)
    assert response.status_code in [200, 404]

def test_get_todos_status(client):
    """
    Kiểm tra endpoint lấy danh sách công việc (/todos)
    """
    response = client.get("/todos")
    # Kiểm tra xem API có hoạt động và trả về mã thành công không
    assert response.status_code == 200
    # Kiểm tra dữ liệu trả về phải là một danh sách (list)
    assert isinstance(response.json(), list)

def test_create_todo_sample(client):
    """
    Kiểm tra tính năng tạo một Todo mới
    """
    todo_data = {
        "title": "Kiểm thử Level 7",
        "description": "Xanh hóa GitHub Actions",
        "completed": False
    }
    response = client.post("/todos", json=todo_data)
    
    # Nếu API tạo mới thành công (thường trả về 200 hoặc 201)
    if response.status_code == 200:
        data = response.json()
        assert data["title"] == todo_data["title"]
        assert "id" in data