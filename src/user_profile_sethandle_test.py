""""
user_profile_sethandle

Takes in (token, handle_str)
Returns {}

Description: Update the authorised user's handle (i.e. display name)

Exceptions:
- InputError when any of:
    - handle_str is not between 3 and 20 characters
    - handle is already in use by another user
"""


import pytest
from auth import auth_register
from user import user_profile, user_profile_sethandle
from error import InputError
from other import clear
from conftest import user_a, user_b


def test_user_profile_sethandle_success(user_a):
    """
    Test 1 - Success when updating a new valid handle
    """
    # New handle_str
    user_a_handle = "kentrellnew"

    # Update user_a's handle with new one
    user_profile_sethandle(user_a["token"], user_a_handle)

    # Receive user_a's profile from function
    check_a = user_profile(user_a["token"], user_a["u_id"])

    # Check
    assert check_a["user"]["handle_str"] == "kentrellnew"

    clear()


def test_user_profile_sethandle_fail(user_a):
    """
    Test 2 - InputError - Invalid handle
    """
    # Invalid handle provided
    user_test_handle = "verylonghandlethatwontwork"

    # Handle length is greater than 20 characters
    with pytest.raises(InputError, match=r"Handle should be between 2 and 20 characters long"):
        user_profile_sethandle(user_a["token"], user_test_handle)

    clear()


def test_user_profile_sethandle_fail_two(user_b):
    """
    Test 3 - InputError - Invalid handle
    """
    # Invalid handle provided
    user_test_handle = "k"

    # Handle length is less than 2 characters
    with pytest.raises(InputError, match=r"Handle should be between 2 and 20 characters long"):
        user_profile_sethandle(user_b["token"], user_test_handle)

    clear()


def test_user_profile_sethandle_duplicate(user_a, user_b):
    """
    Test 4 - InputError - Duplicate handle
    """
    # Duplicate handle provided
    user_b_handle = "kentrellgaulden"

    # Handle is already used by another user
    with pytest.raises(InputError, match=r"Handle taken by another user"):
        user_profile_sethandle(user_b["token"], user_b_handle)

    clear()
