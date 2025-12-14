def test_update_sweet_updates_fields(client, auth_headers):
    # create sweet
    create_response = client.post(
        "/api/sweets",
        json={
            "name": "Barfi",
            "category": "Indian",
            "price": 15.0,
            "quantity": 50,
        },
        headers=auth_headers,
    )

    sweet_id = create_response.json()["id"]

    # update sweet
    update_response = client.put(
        f"/api/sweets/{sweet_id}",
        json={
            "name": "Chocolate Barfi",
            "category": "Indian",
            "price": 20.0,
            "quantity": 40,
        },
        headers=auth_headers,
    )

    assert update_response.status_code == 200
    body = update_response.json()

    assert body["name"] == "Chocolate Barfi"
    assert body["price"] == 20.0
    assert body["quantity"] == 40
