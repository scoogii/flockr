"""
user_profile_http_test.py

Testing that user_profile works with
http implementation
"""


import pytest
import requests
from echo_http_test import url
from conftest_http import user_a
from http_user_functions import http_user_profile



def test_user_profile_http_success(url, user_a):
    """
    Test 1 - Successful return data
    """

    # Request user_a's profile
    payload = http_user_profile(url, user_a["token"], user_a["u_id"])

    result = payload.json()

    assert result == {
        "user": {
            "u_id": 1,
            "email": "nbayoungboy@gmail.com",
            "name_first": "Kentrell",
            "name_last": "Gaulden",
            "handle_str": "kentrellgaulden",
            "profile_img_url": None,
        }
    }


def test_user_profile_http_invalid_token(url, user_a):
    """
    Test 2 - System Error - Invalid Token
    """
    # Invalid token provided
    payload = http_user_profile(url, 348191483, user_a["u_id"])

    assert payload.status_code == 400


def test_user_profile_http_invalid_uid(url, user_a):
    """
    Test 3 - System Error - Invalid UID
    """
    # Invalid UID provided
    payload = http_user_profile(url, user_a["token"], 5)

    assert payload.status_code == 400
