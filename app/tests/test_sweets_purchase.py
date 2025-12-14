def test_purchase_sweet_decreases_quantity(client, auth_headers):
    # create sweet
    create_response = client.post(
        "/api/sweets",
        json={
            "name": "Peda",
            "category": "Indian",
            "price": 6.0,
            "quantity": 10,
        },
        headers=auth_headers,
    )

    sweet_id = create_response.json()["id"]

    # purchase sweet
    purchase_response = client.post(
        f"/api/sweets/{sweet_id}/purchase",
        headers=auth_headers,
    )

    assert purchase_response.status_code == 200

    # list sweets and check quantity
    list_response = client.get(
        "/api/sweets",
        headers=auth_headers,
    )

    sweet = next(s for s in list_response.json() if s["id"] == sweet_id)
    assert sweet["quantity"] == 9
