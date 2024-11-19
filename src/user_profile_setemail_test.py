"""
user_profile_setemail

Takes in parameter `token` and `email`
Returns a an empty dictionary {}

Description: Update the authorised user's email address

Exceptions:
 - InputError - should occur when:
    - Email entered is not a valid email (not valid format)
    - Email address is already being used by another user
"""


import pytest
from auth import auth_register
from user import user_profile, user_profile_setemail
from error import InputError
from other import clear
from conftest import user_a


def test_user_profile_setemail_success(user_a):
    """
    Test 1 - User successfully setting a new email
    """
    # Change email for user_a
    user_profile_setemail(user_a["token"], "nbayoungboynewmail@gmail.com")

    check_a = user_profile(user_a["token"], user_a["u_id"])
    assert check_a["user"]["email"] == "nbayoungboynewmail@gmail.com"

    clear()


def test_multiple_email_change(user_a):
    """
    Test 2 - User successfully sets new email multiple times
    """
    user_profile_setemail(user_a["token"], "change1@gmail.com")
    user_profile_setemail(user_a["token"], "change2@gmail.com")
    user_profile_setemail(user_a["token"], "change3@gmail.com")
    user_profile_setemail(user_a["token"], "change4@gmail.com")

    check_a = user_profile(user_a["token"], user_a["u_id"])
    assert check_a["user"]["email"] == "change4@gmail.com"

    clear()


def test_user_profile_setemail_invalid_email_1(user_a):
    """
    Test 3 - InputError - Invalid email type (domain)
    """
    with pytest.raises(InputError, match=r"Email is invalid"):
        user_profile_setemail(user_a["token"], "invald.com")

    clear()


def test_user_profile_setemail_invalid_email_2(user_a):
    """
    Test 4 - InputError - Invalid email type (no domain)
    """
    with pytest.raises(InputError, match=r"Email is invalid"):
        user_profile_setemail(user_a["token"], "123231312213")

    clear()


def test_user_profile_setemail_empty(user_a):
    """
    Test 5 - InputError - Invalid email type (empty)
    """
    with pytest.raises(InputError, match=r"Email is invalid"):
        user_profile_setemail(user_a["token"], "")

    clear()


def test_user_profile_setemail_duplicate_email(user_a):
    """
    Test 6 - InputError - Email already taken
    """
    with pytest.raises(InputError, match=r"Email taken by another user"):
        user_profile_setemail(user_a["token"], "nbayoungboy@gmail.com")

    clear()
