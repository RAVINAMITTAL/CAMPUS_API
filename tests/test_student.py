def get_token(client):

    login = client.post(
        "/api/v1/auth/login",
        json={
            "username": "pytestuserrr",
            "password": "password12344"
        }
    )

    print("LOGIN")
    print(login.status_code)
    print(login.get_json())

    return login.get_json()["access_token"]

   
def test_invalid_token(client):

    response = client.get(
        "/api/v1/students/detail",
        headers={
            "Authorization": "Bearer invalid_token"
        }
    )

    assert response.status_code == 422


def test_no_token(client):

    response = client.get(
        "/api/v1/students/detail"
    )

    assert response.status_code == 401       
def test_add_student(client):

    token = get_token(client)

    response = client.post(
        "/api/v1/students/fill",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json=[
            {
                "name": "Test Student",
                "email": "teststudent1234@gmail.com",
                "department_id": 1
            }
        ]
    )

    print("ADD STUDENT")
    print(response.status_code)
    print(response.get_json())

    assert response.status_code in [200, 201]
#GET STUDENT 
def test_get_students(client):

    token = get_token(client)

    response = client.get(
        "/api/v1/students/detail",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    print("GET STUDENTS")
    print(response.status_code)
    print(response.get_json())

    assert response.status_code == 200

#GET STUDENT 



def test_logout(client):
    token = get_token(client)

    response = client.post(
        "/api/v1/auth/logout",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200
def test_revoked_token(client):
    token = get_token(client)

    client.post(
        "/api/v1/auth/logout",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    response = client.get(
        "/api/v1/auth/profile",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 401

##refresh token 

def test_refresh(client):

    login = client.post(
        "/api/v1/auth/login",
        json={
            "username":"pytestuserrr",
            "password":"password12344"
        }
    )
    print(login.status_code)
    print(login.get_json())
    refresh_token = login.get_json()["refresh_token"]

    response = client.post(
        "/api/v1/auth/refresh",
        headers={
            "Authorization":
            f"Bearer {refresh_token}"
        }
    )
    
    assert response.status_code == 200
def test_search_student(client):

    token = get_token(client)

    response = client.get(
        "/api/v1/students/search?name=Test",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200    