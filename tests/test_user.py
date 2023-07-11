from datetime import datetime
from datetime import timedelta

import pytest

from .common.user_common import create_test_user
from .common.user_common import delete_test_user
from .common.user_common import get_test_user
from .common.user_common import login_test_user
from models.user_model import CreateUserResponse
from models.user_model import DeleteUserResponse
from models.user_model import GetUserFailureResponse
from models.user_model import GetUserResponse
from models.user_model import LoginResponse

loggedinusertoken = None


def test_createuser():
    """
    This testcase is to check create user api
    """
    print("Starting test: Valid Create User")
    response = create_test_user("createTestUserValid")
    assert isinstance(response, CreateUserResponse)
    assert response.success
    assert response.msg == "User created Successfully: testuser"


def test_createuseralreadyexist():
    """
    This testcase is to check create user api
    for user which already exists
    """
    response = create_test_user("createTestAlreadyExists")
    assert isinstance(response, CreateUserResponse)
    assert not response.success
    assert response.msg.startswith("Username Already Exists")


def test_createuserinvalidusername():
    """
    This testcase is to check regex fail in create user api
    The Username should have 3-20 characters
    """
    response = create_test_user("createTestUserInvalidUsername")
    assert isinstance(response, CreateUserResponse)
    assert not response.success
    assert response.msg.startswith("Invalid Username")


def test_createuserinvalidemail():
    """
    This testcase is to check regex fail in create user api
    The Email should have valid format
    :user!@example.com (Should not contain !)
    """
    response = create_test_user("createTestUserInvalidEmail")
    assert isinstance(response, CreateUserResponse)
    assert not response.success
    assert response.msg.startswith("Invalid Email")


def test_loginuservalid():
    """
    This testcase is to check the login api where parameters
    are valid username and password
    """
    global loggedinusertoken
    response = login_test_user("loginTestUserValid")
    assert isinstance(response, LoginResponse)
    assert response.success
    assert response.msg.startswith("Login Successful")
    loggedinusertoken = response.token


def test_getuser():
    """
    This testcase is to check get user api
    """
    response = get_test_user(loggedinusertoken)
    assert isinstance(response, GetUserResponse)
    assert response.success
    assert response.data.username == "testuser"


def test_loginuserinvalidusername():
    """
    This testcase is to check the login api where parameters
    are Invalid username and password (Not registered)
    """
    response = login_test_user("loginTestUserInvalidUsername")
    assert isinstance(response, LoginResponse)
    assert not response.success
    assert response.msg.startswith("Login Failure Invalid Username")


def test_loginuserpasswordmismatch():
    """
    This testcase is to check the login api where parameters
    are Invalid username and password (Not registered)
    """
    response = login_test_user("loginTestUserPasswordMismatch")
    assert isinstance(response, LoginResponse)
    assert not response.success
    assert response.msg.startswith("Incorrect Password")


def test_getuserexpiredtoken():
    """
    This testcase is to check get user api
    which doesn't exist
    """
    exp_time = datetime.utcnow() - timedelta(minutes=30)
    user_login = login_test_user("loginTestUserValid", exp_time=exp_time)
    response = get_test_user(token=user_login.token)
    assert isinstance(response, GetUserFailureResponse)
    assert not response.success
    assert response.error.startswith("Token has expired")


def test_getuserinvalidtoken():
    """
    This testcase is to check get user api
    which doesn't exist
    """
    response = get_test_user(token="12345")
    assert isinstance(response, GetUserFailureResponse)
    assert not response.success
    assert response.error.startswith("Invalid Token")


def test_deleteuser():
    """
    This testcase is to check delete user api
    """
    response = delete_test_user("deleteTestUser")
    assert isinstance(response, DeleteUserResponse)
    assert response.success
    assert response.msg == "User is deleted."


def test_deleteuserdontexist():
    """
    This testcase is to check delete user api
    which doesn't exists
    """
    response = delete_test_user("deleteTestUserDontExists")
    assert isinstance(response, DeleteUserResponse)
    assert not response.success
    assert response.msg == "User is not registered to delete."


# Run the tests
if __name__ == "__main__":
    pytest.main([__file__])
