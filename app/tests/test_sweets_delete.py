def test_delete_sweet_requires_admin(client, auth_headers):
    # create sweet
    create_response = client.post(
        "/api/sweets",
        json={
            "name": "Jalebi",
            "category": "Indian",
            "price": 5.0,
            "quantity": 30,
        },
        headers=auth_headers,
    )

    sweet_id = create_response.json()["id"]

    # try deleting as non-admin
    delete_response = client.delete(
        f"/api/sweets/{sweet_id}",
        headers=auth_headers,
    )

    assert delete_response.status_code == 403


def test_admin_can_delete_sweet(client):
    # register admin
    client.post(
        "/api/auth/register",
        json={
            "email": "admin@example.com",
            "password": "password123",
            "is_admin": True,
        },
    )

    # login admin
    login_response = client.post(
        "/api/auth/login",
        json={
            "email": "admin@example.com",
            "password": "password123",
        },
    )

    admin_headers = {
        "Authorization": f"Bearer {login_response.json()['access_token']}"
    }

    # create sweet
    create_response = client.post(
        "/api/sweets",
        json={
            "name": "Rasgulla",
            "category": "Indian",
            "price": 8.0,
            "quantity": 25,
        },
        headers=admin_headers,
    )

    sweet_id = create_response.json()["id"]

    # delete sweet as admin
    delete_response = client.delete(
        f"/api/sweets/{sweet_id}",
        headers=admin_headers,
    )

    assert delete_response.status_code == 200


def test_delete_nonexistent_sweet_returns_404(client):
    # register admin
    client.post(
        "/api/auth/register",
        json={
            "email": "admin2@example.com",
            "password": "password123",
            "is_admin": True,
        },
    )

    # login admin
    login_response = client.post(
        "/api/auth/login",
        json={
            "email": "admin2@example.com",
            "password": "password123",
        },
    )

    admin_headers = {
        "Authorization": f"Bearer {login_response.json()['access_token']}"
    }

    # delete non-existent sweet
    response = client.delete(
        "/api/sweets/99999",
        headers=admin_headers,
    )

    assert response.status_code == 404

