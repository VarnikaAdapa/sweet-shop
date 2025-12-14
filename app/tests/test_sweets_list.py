def test_list_sweets_requires_auth(client):
    response = client.get("/api/sweets")
    assert response.status_code == 401


def test_list_sweets_with_auth_returns_list(client, auth_headers):
    response = client.get("/api/sweets", headers=auth_headers)

    assert response.status_code == 200
    assert isinstance(response.json(), list)
