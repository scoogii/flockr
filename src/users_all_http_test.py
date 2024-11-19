"""
users_all_http_test.py

Testing that users_all works with
http implementation
"""


import pytest
import requests
from echo_http_test import url
from conftest_http import user_a, user_b, user_c
from http_other_functions import http_users_all


def test_users_all_http_success(url, user_a, user_b, user_c):
    """
    Test 1 - Success case
    """
    # Request users_all data
    payload = http_users_all(url, user_a["token"])
    profile = payload.json()

    assert profile == {
        'users': [
            {
                'u_id': 1,
                'email': 'nbayoungboy@gmail.com',
                'name_first': 'Kentrell',
                'name_last': 'Gaulden',
                'handle_str': 'kentrellgaulden',
                'profile_img_url': None,
            },
            {
                'u_id': 2,
                'email': 'jerrychan@gmail.com',
                'name_first': 'Jerry',
                'name_last': 'Chan',
                'handle_str': 'jerrychan',
                'profile_img_url': None,
            },
            {
                'u_id': 3,
                'email': 'jamalmurray27@gmail.com',
                'name_first': 'Jamal',
                'name_last': 'Murray',
                'handle_str': 'jamalmurray',
                'profile_img_url': None,
            }
        ],
    }


def test_users_all_http_invalid_token(url):
    """
    Test 2 - System Error - Invalid token
    """
    # Invalid token inputted
    payload = http_users_all(url, "random")

    assert payload.status_code == 400
