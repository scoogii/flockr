"""
user_profile_setname

Takes in (token, name_first, name_last)
Returns {}

Description: Update the authorised user's first and last name

Exceptions:
- InputError when any of:
    - name_first is not between 1 and 50 characters inclusively in length
    - name_last is not between 1 and 50 characters inclusively in length
"""


import pytest
from auth import auth_register
from user import user_profile, user_profile_setname
from error import InputError, AccessError
from other import clear
from conftest import user_a, user_b, user_c


def test_user_profile_setname_success(user_a):
    """
    Test 1 - Success when updating both names
    """
    # Set user_a's name
    user_profile_setname(user_a["token"], "Ken", "Gaulden")

    # Receive user_a's profile from function
    check_a = user_profile(user_a["token"], user_a["u_id"])

    #Check
    assert check_a["user"]["name_first"] == "Ken"
    assert check_a["user"]["name_last"] == "Gaulden"

    clear()


def test_user_profile_setname_success_two(user_b):
    """
    Test 2 - Success when updating both names
    """
    # Receiver user_b's from function
    check_b1 = user_profile(user_b["token"], user_b["u_id"])

    # Set user_b's name
    user_profile_setname(user_b["token"], "Joshua", "Smith")

    # Receive user_b's profile from function after change
    check_b2 = user_profile(user_b["token"], user_b["u_id"])

    # Check
    assert check_b1["user"]["name_first"] != check_b2["user"]["name_first"]
    assert check_b1["user"]["name_last"] != check_b2["user"]["name_last"]

    clear()


def test_user_profile_setname_success_multiple(user_c):
    """
    Test 3 - Success when updating both names multiple time
    """

    # Set user_c's name mutliple time
    user_profile_setname(user_c["token"], "JJ", "Smite")
    user_profile_setname(user_c["token"], "Jeffy", "Smithy")
    user_profile_setname(user_c["token"], "Jay", "Cool")
    user_profile_setname(user_c["token"], "Jay", "Is-Cool")

    # Recieve user_c's profile from function after change
    check_c = user_profile(user_c["token"], user_c["u_id"])

    # Check
    assert check_c["user"]["name_first"] == "Jay"
    assert check_c["user"]["name_last"] == "Is-Cool"

    clear()


def test_setname_first_long(user_a):
    """
    Test 4 - InputError - Invalid name length
    """
    # Length of first name is greater than 50 characters
    with pytest.raises(InputError, match=r"Name must be between 1 and 50 characters inclusive"):
        user_profile_setname(user_a["token"], "verylongfirstname" * 5, "Gaulden")

    clear()


def test_setname_first_short(user_a):
    """
    Test 5 - InputError - Invalid name length
    """
    # First name is empty
    with pytest.raises(InputError, match=r"Name must be between 1 and 50 characters inclusive"):
        user_profile_setname(user_a["token"], "", "Gaulden")

    clear()


def test_setname_last_long(user_b):
    """
    Test 6 - InputError - Invalid name length
    """
    # Length of last name is greater than 50 characters
    with pytest.raises(InputError, match=r"Name must be between 1 and 50 characters inclusive"):
        user_profile_setname(user_b["token"], "Jerry", "verylonglastname" * 5)

    clear()


def test_setname_last_short(user_b):
    """
    Test 7 - Invalid name length
    """
    # Last name is empty
    with pytest.raises(InputError, match=r"Name must be between 1 and 50 characters inclusive"):
        user_profile_setname(user_b["token"], "Jerry", "")

    clear()


def test_user_profile_setname_token():
    """
    Test 8 - Invalid Token
    """
    # User token is invalid
    with pytest.raises(AccessError, match=r"Invalid Token"):
        user_profile_setname("random", "Geoffery", "Smith")

    clear()
