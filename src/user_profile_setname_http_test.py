"""
user_profile_setname_http_test.py

Testing that user_profile_setname works with
http
"""


import pytest
import requests
from echo_http_test import url
from conftest_http import user_a, user_b, user_c
from http_user_functions import http_user_profile, http_user_profile_setname


def test_setname_http_first_success(url, user_a):
    """
    Test 1 - Success when updating First Name
    """
    # Change first name
    http_user_profile_setname(url, user_a["token"], "K", "Gaulden")

    # Request user/profile to get information
    payload = http_user_profile(url, user_a["token"], user_a["u_id"])

    user_a_profile = payload.json()

    assert user_a_profile["user"]["name_first"] == "K"


def test_setname_http_last_success(url, user_b):
    """
    Test 2 - Success when updating Last Name
    """
    # Change last name
    http_user_profile_setname(url, user_b["token"], "Jerry", "C")

    # Request user/profile to get information
    payload = http_user_profile(url, user_b["token"], user_b["u_id"])

    user_b_profile = payload.json()

    assert user_b_profile["user"]["name_last"] == "C"


def test_setname_http_success_multiple(url, user_c):
    """
    Test 3 - Sucess when updating multiple times
    """
    # Change name multiple times
    http_user_profile_setname(url, user_c["token"], "JJ", "Smite")
    http_user_profile_setname(url, user_c["token"], "Jeffy", "Smithy")
    http_user_profile_setname(url, user_c["token"], "Jay", "Cool")

    # Request user/profile to get information
    payload = http_user_profile(url, user_c["token"], user_c["u_id"])

    user_c_profile = payload.json()

    assert user_c_profile["user"]["name_first"] == "Jay"
    assert user_c_profile["user"]["name_last"] == "Cool"


def test_setname_http_first_long(url, user_a):
    """
    Test 4 - System Error - Invalid name length
    """
    # Provide invalid first name
    payload = http_user_profile_setname(url, user_a["token"], "verylongfirstname" * 5, "Gaulden")

    # First name is greater than 50 characters
    assert payload.status_code == 400


def test_setname_http_first_short(url, user_a):
    """
    Test 5 - System Error - Invalid name length
    """
    # Provide invalid first name
    payload = http_user_profile_setname(url, user_a["token"], "", "Gaulden")

    # First name is less than 1 character
    assert payload.status_code == 400


def test_setname_http_last_long(url, user_a):
    """
    Test 6 - System Error - Invalid name length
    """
    # Provide invalid last name
    payload = http_user_profile_setname(url, user_a["token"], "Kentrell", "verylonglastname" * 5)

    # Last name is greater than 50 characters
    assert payload.status_code == 400


def test_setname_http_last_short(url, user_a):
    """
    Test 7 - System Error - Invalid name length
    """
    # Provide invalid last name
    payload = http_user_profile_setname(url, user_a["token"], "Kentrell", "")

    # Last name is less than 1 character
    assert payload.status_code == 400


def test_user_profile_http_setname_token(url, user_a):
    """
    Test 8 - System Error - Invalid Token
    """
    # Provide invalid token
    payload = http_user_profile_setname(url, "random", "Kentrell", "Gaulden")

    # Token is invalid
    assert payload.status_code == 400
