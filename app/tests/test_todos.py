import pytest

# Helper function để lấy Token cho các bài test
def get_auth_headers(client, username, password):
    client.post("/api/v1/auth/register", json={"username": username, "password": password})
    response = client.post("/api/v1/auth/login", data={"username": username, "password": password})
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

# 1. Test tạo To-do thành công
def test_create_todo(client):
    headers = get_auth_headers(client, "user1", "pass123")
    response = client.post(
        "/api/v1/todos/",
        json={"title": "Test Todo", "description": "Nội dung test"},
        headers=headers
    )
    assert response.status_code == 201
    assert response.json()["title"] == "Test Todo"

# 2. Test tính riêng tư (Data Isolation) - QUAN TRỌNG NHẤT
def test_todo_isolation(client):
    # User 1 tạo 1 công việc
    headers1 = get_auth_headers(client, "user1", "pass1")
    client.post("/api/v1/todos/", json={"title": "Task of User 1"}, headers=headers1)

    # User 2 đăng nhập và lấy danh sách
    headers2 = get_auth_headers(client, "user2", "pass2")
    response = client.get("/api/v1/todos/", headers=headers2)

    # User 2 không được thấy công việc của User 1
    assert response.status_code == 200
    assert len(response.json()["items"]) == 0 

# 3. Test lỗi 401 khi không có Token
def test_get_todos_unauthorized(client):
    response = client.get("/api/v1/todos/")
    assert response.status_code == 401