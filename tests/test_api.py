from fastapi.testclient import TestClient


def test_create_user(client: TestClient):
    user_data = {"username": "testuser", "password": "password"}
    response = client.post("/users/", json=user_data)

    assert response.status_code == 200
    assert response.json() == {'id': 1, 'username': 'testuser'}


def test_get_user_non_existing(client: TestClient):
    response = client.get("/users/?username=user_non_exist")

    assert response.status_code == 404
    assert response.json() == {
        "message": "El usuario no existe"
    }
