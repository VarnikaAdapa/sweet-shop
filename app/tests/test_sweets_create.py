def test_create_sweet_requires_auth(client):
    payload = {
        "name": "Ladoo",
        "category": "Indian",
        "price": 10.0,
        "quantity": 100,
    }

    response = client.post("/api/sweets", json=payload)

    assert response.status_code == 401


def test_create_sweet_with_auth_succeeds(client, auth_headers):
    payload = {
        "name": "Ladoo",
        "category": "Indian",
        "price": 10.0,
        "quantity": 100,
    }

    response = client.post(
        "/api/sweets",
        json=payload,
        headers=auth_headers
    )

    assert response.status_code == 201