"""
channels_create_http_test

Testing that channel_invite works with
http implementation
"""


import pytest
import requests
from echo_http_test import url
from conftest_http import user_a, user_b
from http_channels_functions import http_channels_create, http_channels_listall


def test_channels_create_http_public_success(url, user_a):
    """
    Test 1 - Test that public channels are successfully created
    """
    # User_a makes a public channel
    channel_1 = http_channels_create(url, user_a["token"], "billionaire records", True).json()
    c_id_1 = channel_1["channel_id"]

    # If channel was successfully created, it should show using listall
    channels_list = http_channels_listall(url, user_a["token"]).json()

    assert channels_list == {
        "channels": [
            {
                "channel_id": c_id_1,
                "name": "billionaire records",
            },
        ]
    }


def test_channels_create_http_private_success(url, user_a):
    """
    Test 2 - Test that private channels are successfully added
    """
    # User_a makes a public channel
    channel_1 = http_channels_create(url, user_a["token"], "the cage", False).json()
    c_id_1 = channel_1["channel_id"]

    # If channel was successfully added, it should show using listall
    channel_list = http_channels_listall(url, user_a["token"]).json()

    assert channel_list == {
        "channels": [
            {
                "channel_id": c_id_1,
                "name": "the cage",
            },
        ]
    }


def test_channels_create_http_too_long_just_above(url, user_a):
    """
    Test 3 - System Error - name too long, just above maximum
    """
    # User_a makes a public channel
    payload = http_channels_create(url, user_a["token"], 21 * "A", True)
    assert payload.status_code == 400


def test_channels_create_http_too_long_excessive(url, user_a):
    """
    Test 4 - System Error - name too long, excessive number of characters
    """
    # User_a makes a public channel
    payload = http_channels_create(url, user_a["token"], 50 * "A", True)
    assert payload.status_code == 400


def test_channels_create_http_invalid_token(url):
    """
    Test 5 - System Error - Invalid token passed in
    """
    # Error should be raised since token passed is invalid
    invalid_token = ""
    payload = http_channels_create(url, invalid_token, "billionaire records", True)
    assert payload.status_code == 400
