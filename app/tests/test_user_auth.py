import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models.users import UserCreate, User

client = TestClient(app)


@pytest.fixture
def test_register_user():
    username = "testuser"
    email = "testuser@example.com"
    password = "password123"
    user_data = {"username": username, "email": email, "password": password}
    response = client.post("/users", json=user_data)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == username
    assert data["email"] == email
    return data


def test_login_user(test_register_user):
    email = test_register_user["email"]
    password = "password123"
    login_request = {"username": None, "email": email, "password": password}
    response = client.post("/login", json=login_request)
    assert response.status_code == 200
