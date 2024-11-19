"""
user_profile_sethandle_http_test.py

Testing that user_profile_sethandle works with
http implementation
"""


import pytest
import requests
from echo_http_test import url
from conftest_http import user_a, user_b
from http_user_functions import http_user_profile, http_user_profile_sethandle


def test_user_profile_sethandle_http_success(url, user_a):
    """
    Test 1 - Successful request updating a new valid handle
    """
    # Request sent to update handle
    http_user_profile_sethandle(url, user_a["token"], "kentrellnew")

    payload = http_user_profile(url, user_a["token"], user_a["u_id"])

    check_a = payload.json()

    assert check_a["user"]["handle_str"] == "kentrellnew"


def test_user_profile_sethandle_http_fail(url, user_a):
    """
    Test 2 - System Error - Invalid handle
    """
    # Cannot update handle as it is invalid
    payload = http_user_profile_sethandle(url, user_a["token"], "verrylonghandlethatwontwork")

    assert payload.status_code == 400


def test_user_profile_sethandle_http_fail_two(url, user_a):
    """
    Test 3 - System Error - Invalid handle
    """
    payload = http_user_profile_sethandle(url, user_a["token"], "k")

    assert payload.status_code == 400


def test_user_profile_sethandle_duplicate(url, user_a, user_b):
    """
    Test 4 - System Error - Duplicate handle
    """
    # Cannot update handle as it is already in use
    payload = http_user_profile_sethandle(url, user_a["token"], "kentrellgaulden")

    assert payload.status_code == 400
