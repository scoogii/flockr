"""
auth_register_http_test

Testing that auth_register works with
http implementation
"""

import pytest
import requests
from echo_http_test import url
from http_auth_functions import http_auth_register
from http_user_functions import http_user_profile


def test_register_http_returns(url):
    """
    Test 1 - A simple test that checks there are return values for the function
    """
    # Set info about user to pass into server
    email = "nbayoungboy@gmail.com"
    password = "youngboynba123"
    name_first = "Kentrell"
    name_last = "Gaulden"

    payload = http_auth_register(url, email, password, name_first, name_last)

    user_a = payload.json()
    # Assert that a u_id and token is returned
    assert user_a["token"] is not None
    assert user_a["u_id"] is not None


def test_register_http_double(url):
    """
    Test 2 - Test that checks two users are returned unique tokens and u_id's (not the same)
    """
    # Set info for user_b to pass into server
    email_1 = "jerrychan@gmail.com"
    password_1 = "w89rfh@fk"
    name_first_1 = "Jerry"
    name_last_1 = "Chan"

    # Set info for user_c to pass into server
    email_2 = "jamalmurray27@gmail.com"
    password_2 = "NuggetsInFive41"
    name_first_2 = "Jamal"
    name_last_2 = "Murray"

    payload1 = http_auth_register(url, email_1, password_1, name_first_1, name_last_1)
    payload2 = http_auth_register(url, email_2, password_2, name_first_2, name_last_2)

    user_b = payload1.json()
    user_c = payload2.json()

    # Assert that a u_id and token is between two users is unique
    assert user_b["token"] != user_c["token"]
    assert user_b["u_id"] != user_c["u_id"]


def test_register_profile_http(url):
    """
    Test 3 - Test that uses user/profile to check information was added correctly
             and handle was formed
    """
    # Set info to user_d pass into server
    email = "jeffsmithiscool@gmail.com"
    password = "smithjeff"
    name_first = "Jeff"
    name_last = "Smith"

    # Register the user
    payload = http_auth_register(url, email, password, name_first, name_last)
    user_d = payload.json()

    # Get the token and u_id from when the user registered
    # Use user_profile to check information was added correctly
    payload = http_user_profile(url, user_d["token"], user_d["u_id"])

    user_d_profile = payload.json()
    assert user_d_profile == {
        "user": {
            "u_id": 1,
            "email": "jeffsmithiscool@gmail.com",
            "name_first": "Jeff",
            "name_last": "Smith",
            "handle_str": "jeffsmith",
            "profile_img_url": None,
        }
    }


# InputError Tests (http)
def test_invalid_email_http(url):
    """
    Test 4 - Check that entering an incorrect email will raise an error
    """
    # Information to register a user (contains invalid email)
    invalid_email = "abc.com"
    password = "ksgnflnwlfwk"
    name_first = "Bill"
    name_last = "Pot"

    # Register the user
    payload = http_auth_register(url, invalid_email, password, name_first, name_last)

    assert payload.status_code == 400


def test_used_email_http(url):
    """
    Test 5 - Check that duplicate emails are not allowed (email already used by another user)
    """
    # Information to register a user
    email_1 = "nbayoungboy@gmail.com"
    password_1 = "jkbbjbfgn"
    name_first_1 = "Kentrell"
    name_last_1 = "Gaulden"

    # Register the user - valid
    payload = http_auth_register(url, email_1, password_1, name_first_1, name_last_1)

    # The same email is used again
    used_email = "nbayoungboy@gmail.com"
    password_2 = "jkbbjbfgn"
    name_first_2 = "K"
    name_last_2 = "Gaulden"

    # Register the user -> invalid
    payload = http_auth_register(url, used_email, password_2, name_first_2, name_last_2)

    assert payload.status_code == 400


def test_invalid_password_http(url):
    """
    Test 6 - Check that an error is raised for an incorrect password
    """
    # Information to register a user (contains password that is too short)
    email = "abc@gmail.com"
    password = "sd"
    name_first = "Short"
    name_last = "Short"

    # Register the user -> invalid
    payload = http_auth_register(url, email, password, name_first, name_last)

    assert payload.status_code == 400


def test_invalid_first_name_http(url):
    """
    Test 7 - Check that error is raised for invalid length of first name
    """
    # Information to register a user (contains first-name that is too short)
    email = "hi@gmail.com"
    password = "abcdefghijklmnop"
    invalid_name_first = ""
    name_last = "Empty"

    # Register the user -> invalid
    payload = http_auth_register(url, email, password, invalid_name_first, name_last)

    assert payload.status_code == 400


def test_invalid_last_name_http(url):
    """
    Test 8 - Check that error is raised for invalid length of last name
    """
    # Information to register a user (contains last-name that is too long)
    email = "hi@gmail.com"
    password = "abcdefghijklmnop"
    name_first = "Long"
    invalid_name_last = "abc" * 20

    # Register the user -> invalid
    payload = http_auth_register(url, email, password, name_first, invalid_name_last)

    assert payload.status_code == 400
