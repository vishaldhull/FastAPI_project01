from .utils import *
from fastapi import status
from ..routers.admin import get_db, get_current_user


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_return_user(test_user):
    response = client.get("/users")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['username'] == "codingwithkabir"
    assert response.json()['email'] == "vinsdeck@gmail.com"
    assert response.json()['first_name'] == "kabir"
    assert response.json()['last_name'] == "singh"
    assert response.json()['role'] == "admin"
    #assert response.json()['phone_number'] == "1234567890"


def test_change_password_success(test_user):
    response = client.put("/users/change_password", json={"password": "newpassword",
                                                          "new_password": "demo_password1"})
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_change_password_failure(test_user):
    response = client.put("/users/change_password", json={"password": "wrongpassword",
                                                          "new_password": "newpassword"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Error on password change"}


def test_update_phone_number(test_user):
    response = client.put("/users/phonenumber/9876543210")
    assert response.status_code == status.HTTP_204_NO_CONTENT