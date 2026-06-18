def test_home(client):
    response = client.get('/')
    assert response.status_code == 200
def test_register(client):

    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "pytestuserrr",
            "password": "password12344"
        }
    )

    assert response.status_code in [201, 409]    
def test_login(client):

    response = client.post(
        "/api/v1/auth/login",
        json={
            "username": "pytestuserrr",
            "password": "password12344"
        }
    )

    assert response.status_code == 200

    data = response.get_json()

    assert "access_token" in data
    assert "refresh_token" in data
def test_profile(client):

    login = client.post(
        "/api/v1/auth/login",
        json={
            "username": "pytestuserrr",
            "password": "password12344"
        }
    )

    token = login.get_json()["access_token"]

    response = client.get(
        "/api/v1/auth/profile",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200        
    