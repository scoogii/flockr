"""
channel_join_http_test

Testing that channel_join works with
http implementation
"""

import requests
from echo_http_test import url
from conftest_http import user_a, user_b
from http_channel_functions import http_channel_join, http_channel_details
from http_channels_functions import http_channels_create, http_channels_list
from http_user_functions import http_user_profile


def test_channel_join_http_success_1(url, user_a, user_b):
    """
    Test 1 - Testing user that joined is added to channel using channel_details
    """
    # User_a makes a channel
    channel_1 = http_channels_create(url, user_a["token"], "billionaire records", True).json()
    c_id_1 = channel_1["channel_id"]

    http_channel_join(url, user_b["token"], c_id_1)

    # Retrieve user profiles
    user_a_profile = (http_user_profile(url, user_a["token"], user_a["u_id"]).json())["user"]
    user_b_profile = (http_user_profile(url, user_b["token"], user_b["u_id"]).json())["user"]

    channel_details = http_channel_details(url, user_b["token"], c_id_1).json()

    assert channel_details == {
        "name": "billionaire records",
        "owner_members": [
            {
                "u_id": user_a["u_id"],
                "name_first": user_a_profile["name_first"],
                "name_last": user_a_profile["name_last"],
                "profile_img_url": user_a_profile["profile_img_url"],
            }
        ],
        "all_members": [
            {
                "u_id": user_a["u_id"],
                "name_first": user_a_profile["name_first"],
                "name_last": user_a_profile["name_last"],
                "profile_img_url": user_a_profile["profile_img_url"],
            },
            {
                "u_id": user_b["u_id"],
                "name_first": user_b_profile["name_first"],
                "name_last": user_b_profile["name_last"],
                "profile_img_url": user_b_profile["profile_img_url"],
            },
        ],
    }


def test_channel_join_http_success_2(url, user_a, user_b):
    """
    Test 2 - Testing user that joined is added to channel using channels_list
    """
    # User_a makes a channel
    channel_1 = http_channels_create(url, user_a["token"], "billionaire records", True).json()
    c_id_1 = channel_1["channel_id"]

    # User_b joins channel
    http_channel_join(url, user_b["token"], c_id_1)

    channel_list = http_channels_list(url, user_b["token"]).json()

    assert channel_list == {
        "channels": [
            {
                "channel_id": c_id_1,
                "name": "billionaire records",
            }
        ],
    }


def test_channel_join_http_invalid_channel_id(url, user_a):
    """
    Test 3 - System Error - for invalid channel ID
    """
    # User_a cannot join because the channel ID is invalid
    invalid_c_id = 4566343
    payload = http_channel_join(url, user_a["token"], invalid_c_id)

    assert payload.status_code == 400


def test_channel_join_http_private(url, user_a, user_b):
    """
    Test 4 - System Error - for when user is not authorised to join channel
    """
    # User_a makes a channel
    channel_1 = http_channels_create(url, user_a["token"], "billionaire records", False).json()
    c_id_1 = channel_1["channel_id"]

    # Error should be raised because user_b is not authorised to join
    payload = http_channel_join(url, user_b["token"], c_id_1)

    assert payload.status_code == 400


def test_channel_join_http_invalid_token(url, user_a):
    """
    Test 5 - System Error - Invalid token is passed in
    """
    # User_a makes a channel
    channel_1 = http_channels_create(url, user_a["token"], "billionaire records", True).json()
    c_id_1 = channel_1["channel_id"]

    # Error should be raised because token is invalid
    invalid_token = ""
    payload = http_channel_join(url, invalid_token, c_id_1)

    assert payload.status_code == 400
