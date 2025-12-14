from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_current_user_requires_auth():
    response = client.get("/api/me")
    assert response.status_code == 401
