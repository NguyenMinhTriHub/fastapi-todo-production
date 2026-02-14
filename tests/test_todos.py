def test_get_todos_unauthorized(client):
    """Phải trả về 401 khi không có Token"""
    response = client.get("/todos/")
    assert response.status_code == 401

def test_get_todos_empty(client, normal_user_token_headers):
    """Phải trả về 200 khi có Token hợp lệ"""
    response = client.get("/todos/", headers=normal_user_token_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_todo(client, normal_user_token_headers):
    """Kiểm tra tạo Todo thành công"""
    new_todo = {"title": "Test Title", "description": "Test Desc", "completed": False}
    response = client.post("/todos/", json=new_todo, headers=normal_user_token_headers)
    assert response.status_code == 201
    assert response.json()["title"] == "Test Title"