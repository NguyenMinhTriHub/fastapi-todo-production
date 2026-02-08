def test_read_root(client):
    """Kiểm tra xem API trang chủ có phản hồi không"""
    response = client.get("/")
    assert response.status_code == 200
    # Đảm bảo nội dung này khớp với những gì bạn viết trong app/main.py
    assert "message" in response.json()

def test_get_todos(client):
    """Kiểm tra API lấy danh sách todos"""
    response = client.get("/todos")
    assert response.status_code == 200
    assert isinstance(response.json(), list)