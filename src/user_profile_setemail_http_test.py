"""
user_profile_setemail_http_test.py

Testing that user_profile_setemail works with
http
"""


import pytest
import requests
from echo_http_test import url
from conftest_http import user_a, user_b
from http_user_functions import http_user_profile, http_user_profile_setemail


def test_setemail_http_success(url, user_a):
    """
    Test 1 - User successfully setting a new email
    """
    # send request to change the email
    http_user_profile_setemail(url, user_a["token"], "nba@gmail.com")

    # user/profile to get information
    payload = http_user_profile(url, user_a["token"], user_a["u_id"])

    user_a_profile = payload.json()

    assert user_a_profile["user"]["email"] == "nba@gmail.com"


def test_setemail_http_multiple(url, user_b):
    """
    Test 2 - User successfully sets new email multiple times
    """
    # Change emails mutliple times
    http_user_profile_setemail(url, user_b["token"], "jc@gmail.com")
    http_user_profile_setemail(url, user_b["token"], "jerry.chan@gmail.com")
    http_user_profile_setemail(url, user_b["token"], "Jerry123@gmail.com")

    # user/profile to get information
    payload = http_user_profile(url, user_b["token"], user_b["u_id"])

    user_b_profile = payload.json()

    assert user_b_profile["user"]["email"] == "jerry123@gmail.com"


def test_user_profile_setemail_http_invalid_email_1(url, user_a):
    """
    Test 3 - System Error - Invalid email type (domain)
    """
    # Provide invalid email (domain)
    payload = http_user_profile_setemail(url, user_a["token"], "invald.com")

    # Email is not valid
    assert payload.status_code == 400


def test_user_profile_setemail_http_invalid_email_2(url, user_a):
    """
    Test 4 - System Error - Invalid email type (no domain)
    """
    # Provide invalid email (no domain)
    payload = http_user_profile_setemail(url, user_a["token"], "123231312213")

    # Email is not valid
    assert payload.status_code == 400


def test_user_profile_setemail_http_email_empty(url, user_a):
    """
    Test 5 - System Error - Invalid email type (empty)
    """
    # Provide invalid email (empty)
    payload = http_user_profile_setemail(url, user_a["token"], "")

    # Email is not valid
    assert payload.status_code == 400


def test_user_profile_setemail_http_duplicate_email(url, user_a):
    """
    Test 6 - System Error - Duplicate email
    """
    # Provide duplicate email
    payload = http_user_profile_setemail(url, user_a["token"], "nbayoungboy@gmail.com")

    # Email is already being used
    assert payload.status_code == 400
