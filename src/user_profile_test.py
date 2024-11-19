"""
user_profile

Takes in (token, u_d)
Returns { user }

Description: From a valid user, returns information about their user_id,
email, first name, last name, and handle

Exceptions:
- InputError when any of:
    - name_first is not between 1 and 50 characters inclusively in length
    - name_last is not between 1 and 50 characters inclusively in length
"""


import pytest
from auth import auth_register
from user import user_profile
from error import InputError, AccessError
from other import clear
from conftest import user_a, user_b, user_c, user_d, user_e


def test_user_profile_success(user_a):
    """
    Test 1 - Successful return data
    """
    #Check
    assert user_profile(user_a["token"], user_a["u_id"]) == {
        "user": {
            "u_id": user_a["u_id"],
            "email": "nbayoungboy@gmail.com",
            "name_first": "Kentrell",
            "name_last": "Gaulden",
            "handle_str": "kentrellgaulden",
            "profile_img_url": None,
        },
    }

    clear()


def test_user_profile_success_two(user_b):
    """
    Test 2 - Successful return data
    """
    #Check
    assert user_profile(user_b["token"], user_b["u_id"]) == {
        "user": {
            "u_id": user_b["u_id"],
            "email": "jerrychan@gmail.com",
            "name_first": "Jerry",
            "name_last": "Chan",
            "handle_str": "jerrychan",
            "profile_img_url": None,
        },
    }

    clear()


def test_user_profile_success_three(user_c):
    """
    Test 3 - Successful return data
    """
    #Check
    assert user_profile(user_c["token"], user_c["u_id"]) == {
        "user": {
            "u_id": user_c["u_id"],
            "email": "jamalmurray27@gmail.com",
            "name_first": "Jamal",
            "name_last": "Murray",
            "handle_str": "jamalmurray",
            "profile_img_url": None,
        },
    }

    clear()


def test_user_profile_success_four(user_d):
    """
    Test 4 - Successful return data
    """
    #Check
    assert user_profile(user_d["token"], user_d["u_id"]) == {
        "user": {
            "u_id": user_d["u_id"],
            "email": "jeffsmithiscool@gmail.com",
            "name_first": "Jeff",
            "name_last": "Smith",
            "handle_str": "jeffsmith",
            "profile_img_url": None,
        },
    }

    clear()


def test_user_profile_success_five(user_e):
    """
    Test 5 - Successful return data
    """
    #Check
    assert user_profile(user_e["token"], user_e["u_id"]) == {
        "user": {
            "u_id": user_e["u_id"],
            "email": "bobbyjones@gmail.com",
            "name_first": "Bobby",
            "name_last": "Jones",
            "handle_str": "bobbyjones",
            "profile_img_url": None,
        },
    }

    clear()


def test_user_profile_invalid_token(user_a):
    """
    Test 6 - The token does not exist so user_a's profile cannot be retrieved
    """
    with pytest.raises(AccessError, match=r"Invalid Token"):
        user_profile(348191483, user_a["u_id"])

    clear()


def test_user_profile_invalid_uid(user_a):
    """
    Test 7 - The u_id does not exist so cannot be found
    """
    with pytest.raises(InputError, match=r"Invalid User ID"):
        user_profile(user_a["token"], -5)

    clear()
    