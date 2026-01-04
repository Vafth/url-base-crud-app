def test_registration(client):
    response = client.post("/register/",
                           data={"username": "user",
                                 "password": "123"})
    assert response.status_code == 200
    assert response.json() == {
        "messsage": "User user was created successfully",
          "user": {
              "username": "user",
              "is_admin": False,
              "is_disabled": False,
              "id": 1
        }
        
    }

def test_registration_409_error(client, create_user):
    new_user = create_user(username ="user",
                           password= "123")
    
    response = client.post("/register/",
                           data={"username": "user",
                                 "password": "321"})
    assert response.status_code == 409
    assert response.json() == {
        "detail": "Username user is already taken"
    }

def test_login(client, create_user):
    new_user = create_user(username ="user",
                           password= "123")
    client.cookies["access_token"] = new_user["token"]
    
    response = client.post("/login/",
                           data={"username": new_user["username"],
                                 "password": "123"},
                            follow_redirects=False)
    assert response.status_code == 303
    assert response.headers["location"] == "/"


def test_login_401_error(client, create_user):
    new_user = create_user(username ="user",
                           password= "123")
    
    response = client.post("/login/",
                           data={"username": new_user["username"],
                                 "password": "321"},
                            follow_redirects=False)
    assert response.status_code == 401
    assert response.json() == {
        "detail": "Incorrect username or password"
    }


def test_logout(client, create_user):
    new_user = create_user(username ="user",
                           password= "123")
    
    response = client.get("/logout/",
                           follow_redirects=False)
    assert response.status_code == 303
    assert response.headers["location"] == "/login/"
    
    assert client.cookies.get("access_token") == None


def test_logout_401_error(client):
    response = client.get("/logout/",
                           follow_redirects=False)
    assert response.status_code == 401
    assert response.cookies.get("access_token") == None

    assert response.json() == {
        "detail": "Could not validate credentials"
    }