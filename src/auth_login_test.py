"""
auth_login

Takes in parameters `email`, `password`
Returns a dictionary {"u_id", "token"}

Description: Given a valid email and password, logs a user in and returns u_id and token

InputError should occur when:
 - Email entered is not a valid email (format)
 - Email entered does not belong to a user
 - Password is not correct
"""


import pytest
from auth import auth_register, auth_login, auth_logout
from error import InputError
from other import clear


def test_login_success_1():
    """
    Test 1 - testing a user can successfully log in with valid information
    """
    # Registering User with valid information
    user_a = auth_register("nbayoungboy@gmail.com", "youngboynba123", "Kentrell", "Gaulden")
    token_1 = user_a["token"]
    u_id_1 = user_a["u_id"]

    # Logout using users valid token
    auth_logout(token_1)
    # Login user with correct email and password
    login_check_1 = auth_login("nbayoungboy@gmail.com", "youngboynba123")

    # Get u_id and token
    u_id_1 = login_check_1["u_id"]
    token_1 = login_check_1["token"]

    # Assert user has logged in by checking the return values of u_id and token
    assert login_check_1 == {"u_id": u_id_1, "token": token_1}

    clear()


def test_login_success_2():
    """
    Test 2 - testing a user can successfully log in with valid information
    """
    # Registering User with valid information
    user_b = auth_register("jerrychan@gmail.com", "w89rfh@fk", "Jerry", "Chan")
    token_2 = user_b["token"]

    # Logout using users valid token
    auth_logout(token_2)
    login_check_2 = auth_login("jerrychan@gmail.com", "w89rfh@fk")

    # Get u_id and token
    u_id_2 = login_check_2["u_id"]
    token_2 = login_check_2["token"]

    # Assert user has logged in by checking the return values of u_id and token
    assert login_check_2 == {"u_id": u_id_2, "token": token_2}

    clear()


def test_not_same():
    """
    Test 3 - Ensuring two registered users do not return the same information
    """
    # Registering users with valid information
    user_c = auth_register("jeffsmithiscool@gmail.com", "smithjeff", "Jeff", "Smith")
    user_d = auth_register("bobbyjones@gmail.com", "iliketoysandstuff", "  Bobby", "  Jones ")

    # Extracting tokens and logging users out
    token_3 = user_c["token"]
    token_4 = user_d["token"]
    auth_logout(token_3)
    auth_logout(token_4)

    # Using email and password to log in
    user_c2 = auth_login("jeffsmithiscool@gmail.com", "smithjeff")
    user_d2 = auth_login("bobbyjones@gmail.com", "iliketoysandstuff")

    # Checking u_id and token returned is specific to users
    assert user_c2["u_id"] != user_d2["u_id"]
    assert user_c2["token"] != user_d2["token"]

    clear()


# InputError Tests
def test_unregistered_email_1():
    """
    Test 4.1 - Email entered does not belong to a registered user
    """
    with pytest.raises(InputError, match=r"Email does not belong to a user"):
        auth_login("unregistereduser_e@gmail.com", "jkbvlei4")


def test_unregistered_email_2():
    """
    Test 4.2 - Email entered does not belong to a registered user
    """
    with pytest.raises(InputError, match=r"Email does not belong to a user"):
        auth_login("unregistereduser_e@gmail.com", "489ghj")


def test_invalid_email():
    """
    Test 5.1 - Email has invalid format
    """
    user_e = auth_register("invalid@gmail.com", "123abc!@#", "Tim", "Sun")
    token_5 = user_e["token"]
    auth_logout(token_5)

    with pytest.raises(InputError, match=r"Email is invalid"):
        auth_login("invalid.com", "123abc!@#")

    clear()


def test_empty_email():
    """
    Test 5.2 - Email has invalid format - Empty Input test
    """
    user_f = auth_register("emptyemail@gmail.com", "sjdfbjksdb", "Empty", "Email")
    token_6 = user_f["token"]
    auth_logout(token_6)

    with pytest.raises(InputError, match=r"Email is invalid"):
        auth_login("", "sjdfbjksdb")

    clear()


def test_incorrect_password_1():
    """
    Test 6.1 - Password is incorrect - different integers
    """
    user_g = auth_register("forgotpassword@gmail.com", "skgbw4123", "Tess", "Li")
    token_7 = user_g["token"]
    auth_logout(token_7)

    with pytest.raises(InputError, match=r"Incorrect password"):
        auth_login("forgotpassword@gmail.com", "skgbw4129")

    clear()


def test_incorrect_password_2():
    """
    Test 6.2 - Password is incorrect - different case for letters (case-sensitive test)
    """
    user_h = auth_register("casesensitive@gmail.com", "D39hrnfc", "Olivia", "Crane")
    token_8 = user_h["token"]
    auth_logout(token_8)

    with pytest.raises(InputError, match=r"Incorrect password"):
        auth_login("casesensitive@gmail.com", "d39Hrnfc")

    clear()


def test_empty_password():
    """
    Test 6.3 - Password is incorrect - empty input
    """
    user_i = auth_register("emptypassword@gmail.com", "oisewrhf", "Em", "Pass")
    token_9 = user_i["token"]
    auth_logout(token_9)

    with pytest.raises(InputError, match=r"Incorrect password"):
        auth_login("emptypassword@gmail.com", "")

    clear()
