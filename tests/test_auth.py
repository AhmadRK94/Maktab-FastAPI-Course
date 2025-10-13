def test_login_user_ok(client):
    user_login_data = {
        "email": "testuser@example.com",
        "password": "testpassword",
    }
    response = client.post("/auth/login", json=user_login_data)
    assert response.status_code == 200
    assert response.json() == {"detail": "Login successful."}
    assert response.cookies.get("access_token") is not None
    assert response.cookies.get("refresh_token") is not None


def test_logout_user_ok(auth_client):
    response = auth_client.post("/auth/logout")
    assert response.status_code == 200
    assert response.json() == {"detail": "Logout successful."}
    assert response.cookies.get("access_token") is None
    assert response.cookies.get("refresh_token") is None


def test_logout_user_bad(client):
    response = client.post("/auth/logout")
    assert response.status_code == 401
    assert response.json() == {
        "error": True,
        "status_code": 401,
        "detail": "Authentication failed, access token not found.",
    }
    assert response.cookies.get("access_token") is None
    assert response.cookies.get("refresh_token") is None


def test_login_user_400(client):
    user_login_data = {
        "email": "nottestuser@example.com",
        "password": "nottestpassword",
    }
    response = client.post("/auth/login", json=user_login_data)
    assert response.status_code == 400
    assert response.json() == {
        "error": True,
        "status_code": 400,
        "detail": "Invalid Username or Password.",
    }
    assert response.cookies.get("access_token") is None
    assert response.cookies.get("refresh_token") is None
