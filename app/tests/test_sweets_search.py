def test_search_sweets_by_name(client, auth_headers):
    # create sweets
    client.post(
        "/api/sweets",
        json={
            "name": "Rasgulla",
            "category": "Indian",
            "price": 10.0,
            "quantity": 20,
        },
        headers=auth_headers,
    )

    client.post(
        "/api/sweets",
        json={
            "name": "Brownie",
            "category": "Bakery",
            "price": 25.0,
            "quantity": 5,
        },
        headers=auth_headers,
    )

    # search
    response = client.get(
        "/api/sweets/search?name=ras",
        headers=auth_headers,
    )

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Rasgulla"
