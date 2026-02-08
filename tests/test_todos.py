def test_read_main(client):
    """Kiểm tra xem API trang chủ có hoạt động không"""
    response = client.get("/")
    assert response.status_code == 200
    # Nếu bạn đã sửa app/main.py có trả về message
    assert response.json() == {"message": "Application is Live"}

def test_get_todos_empty(client):
    """Kiểm tra danh sách Todo ban đầu phải trống"""
    response = client.get("/todos")
    assert response.status_code == 200
    assert isinstance(response.json(), list)