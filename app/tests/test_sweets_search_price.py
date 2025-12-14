def test_search_sweets_by_price_range(client, auth_headers):
    client.post(
        "/api/sweets",
        json={
            "name": "Ladoo",
            "category": "Indian",
            "price": 5.0,
            "quantity": 10,
        },
        headers=auth_headers,
    )

    client.post(
        "/api/sweets",
        json={
            "name": "Cake",
            "category": "Bakery",
            "price": 50.0,
            "quantity": 5,
        },
        headers=auth_headers,
    )

    response = client.get(
        "/api/sweets/search?min_price=1&max_price=10",
        headers=auth_headers,
    )

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Ladoo"
