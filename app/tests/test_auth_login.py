from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_user_login_returns_jwt_token():
    # First, register a user
    register_payload = {
        "email": "login_test@example.com",
        "password": "password123",
        "is_admin": False
    }
    client.post("/api/auth/register", json=register_payload)

    # Then, login
    login_payload = {
        "email": "login_test@example.com",
        "password": "password123"
    }
    response = client.post("/api/auth/login", json=login_payload)

    assert response.status_code == 200
    body = response.json()
    assert "access_token" in body
    assert body["token_type"] == "bearer"

    data = response.json()
    assert "access_token" in data
