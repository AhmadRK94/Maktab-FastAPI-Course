def test_get_all_expenses_no_auth(client):
    response = client.get("/expenses/")
    assert response.status_code == 401
    assert response.json() == {
        "error": True,
        "status_code": 401,
        "detail": "Authentication failed, access token not found.",
    }


def test_get_all_expenses_auth(auth_client):
    response = auth_client.get("/expenses/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 1


def test_get_expense_auth_ok(auth_client):
    response = auth_client.get("/expenses/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1


def test_get_expense_auth_404(auth_client):
    response = auth_client.get("/expenses/3")
    assert response.status_code == 404
    assert response.json() == {
        "error": True,
        "status_code": 404,
        "detail": "item with id: 3 doesn't exist.",
    }



def test_delete_expense_auth_404(auth_client):
    response = auth_client.delete("/expenses/3")
    assert response.status_code == 404
    assert response.json() == {
        "error": True,
        "status_code": 404,
        "detail": "item with id: 3 doesn't exist.",
    }

def test_get_expense_auth_401(client):
    response = client.get("/expenses/1")
    assert response.status_code == 401
