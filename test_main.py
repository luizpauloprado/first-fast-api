from fastapi.testclient import TestClient
from main import app, db, UserIn

client = TestClient(app)


def test_get_user():
    response = client.get("/users")
    data = response.json()

    assert response.status_code == 200
    assert len(data) == 4
    assert isinstance(data, list)


def test_post_users():
    json_post = {"name": "Lula", "age": 80}
    response = client.post("/users", json=json_post)
    data = response.json()

    assert response.status_code == 200
    assert "id" in data
    assert data["name"] == json_post["name"]
    assert data["age"] == json_post["age"]


def test_post_user_error():
    json_post = {"name": "Lula"}
    response = client.post("/users", json=json_post)
    data = response.json()

    assert response.status_code == 422
    assert data["detail"] != {}


def test_get_user():
    user_id = 1
    response = client.get(f"/users/{user_id}")
    data = response.json()

    assert response.status_code == 200
    assert data["id"] == user_id


def test_get_user_error():
    response = client.get(f"/users/{9999}")
    data = response.json()

    assert response.status_code == 404
    assert data["detail"] != {}


def test_put_user():
    user_id = 1
    json_put = {"name": "LP", "age": 38}
    response = client.put(f"/users/{user_id}", json=json_put)
    data = response.json()

    assert response.status_code == 200
    assert data["id"] == user_id
    assert data["name"] == "LP"
    assert data["age"] == 38


def test_put_user_error():
    user_id = 999
    json_put = {"name": "LP", "age": 38}
    response = client.put(f"/users/{user_id}", json=json_put)
    data = response.json()

    assert response.status_code == 404
    assert data["detail"] != {}


def test_delete_user():
    user_id = 1
    response = client.delete(f"/users/{user_id}")

    assert response.status_code == 200


def test_delete_user_error():
    user_id = 999
    response = client.delete(f"/users/{user_id}")
    data = response.json()

    assert response.status_code == 404
    assert data["detail"] != {}


def test_get_user_search():
    params = {"name": "Lu"}
    response = client.get("/users/search/", params=params)
    data = response.json()

    assert response.status_code == 200
    assert len(data) == 1


def test_get_user_search_error():
    params = {"name": "L"}
    response = client.get("/users/search/", params=params)
    data = response.json()

    assert response.status_code == 422
    assert data["detail"] != {}
