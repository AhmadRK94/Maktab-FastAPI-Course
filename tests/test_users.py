def test_create_user_ok(client):
    user_data = {
        "username": "testuser2",
        "email": "testuser2@example.com",
        "password": "testpassword2",
        "password_confirm": "testpassword2",
    }
    response = client.post("/users/register", json=user_data)
    assert response.status_code == 201
    assert response.json() == {"detail": "User registered successfully."}



def test_create_user_conflict(client):
    user_data = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "testpassword",
        "password_confirm": "testpassword",
    }
    response = client.post("/users/register", json=user_data)
    assert response.status_code == 409
    assert response.json() == {
        "error": True,
        "status_code": 409,
        "detail": f"User with email: {user_data['email'].lower()} is already exist.",
    }


def test_create_user_password_mismatch(client):
    user_data = {
        "username": "testuser2",
        "email": "testuser2@example.com",
        "password": "testpassword2",
        "password_confirm": "testpasswordbad",
    }
    response = client.post("/users/register", json=user_data)
    assert response.status_code == 422


def test_get_all_users(client):
    response = client.get("/users/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 0
