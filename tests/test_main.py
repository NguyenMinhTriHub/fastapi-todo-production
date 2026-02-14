def test_read_main(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Server is running smoothly!"}

# Sửa lỗi 401: Thêm fixture normal_user_token_headers vào hàm
def test_get_todos_status(client, normal_user_token_headers):
    response = client.get("/todos/", headers=normal_user_token_headers)
    assert response.status_code == 200