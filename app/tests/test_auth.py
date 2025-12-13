from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_user_registration():
    payload = {
        "email": "test@example.com",
        "password": "password123",
        "is_admin": False
    }

    response = client.post("/api/auth/register", json=payload)

    assert response.status_code == 201
    assert response.json()["email"] == "test@example.com"
