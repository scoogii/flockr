"""
auth_logout

Takes in Parameters: token
Return Type: is_success

Description: Given an active token, invalidates the token to log the user out.
            Valid token is given -> user is successfully logged out -> returns True
            Invalid token -> returns false
"""

import pytest
from auth import auth_register, auth_login, auth_logout
from other import clear
from error import AccessError


def test_logout_success():
    """
    Test 1 - Tests that a registered user is returned a valid token and can log out
    """
    # Register user a
    user_a = auth_register(
        "nbayoungboy@gmail.com", "youngboynba123", "Kentrell", "Gaulden"
    )
    token_1 = user_a["token"]

    # Logout user using their active token
    assert auth_logout(token_1) == {"is_success": True}

    clear()


def testlogin_logout_loop():
    """
    Test 2 - Tests a registered user can log in and out multiple times but cannot logout twice
    """
    # Registering and logging out
    user_b = auth_register(
        "jamalmurray27@gmail.com", "NuggetsInFive41", "Jamal", "Murray"
    )
    token_2 = user_b["token"]
    auth_logout(token_2)

    # Logging in and out first time
    auth_login("jamalmurray27@gmail.com", "NuggetsInFive41")
    token_2 = user_b["token"]
    auth_logout(token_2)

    # Logging in and out second time
    auth_login("jamalmurray27@gmail.com", "NuggetsInFive41")
    token_2 = user_b["token"]
    assert auth_logout(token_2) == {"is_success": True}

    # Token now invalidated -> raise error
    with pytest.raises(AccessError, match=r"Invalid Token"):
        auth_logout(token_2)

    clear()


def test_logout_invalid_token():
    """
    Test 3 - Testing a range of invalid tokens -> raises AccessError
    """
    with pytest.raises(AccessError, match=r"Invalid Token"):
        auth_logout("token_8")

    # Adding a user - to ensure change to data does not affect logging out
    auth_register("jeffsmithiscool@gmail.com", "smithjeff", "Jeff", "Smith")

    with pytest.raises(AccessError, match=r"Invalid Token"):
        auth_logout(1234567)

    clear()


def test_logout_empty_token():
    """
    Test 4 - Testing empty input -> returns False
    """
    with pytest.raises(AccessError, match=r"Invalid Token"):
        auth_logout("")

    # Adding a user
    auth_register("bobbyjones@gmail.com", "iliketoysandstuff", "Bobby", "Jones")

    with pytest.raises(AccessError, match=r"Invalid Token"):
        auth_logout(" ")

    clear()
