"""
channel_invite_http_test

Testing that channel_invite works with
http implementation
"""


import requests
from echo_http_test import url
from conftest_http import user_a, user_b, user_c
from http_channels_functions import http_channels_create
from http_channel_functions import (
    http_channel_details,
    http_channel_invite,
)
from http_channels_functions import http_channels_list
from http_user_functions import http_user_profile


def test_channel_invite_http_success_1(url, user_a, user_b):
    """
    Test 1 - Checking invited user is part of channel using channel_details
    """
    # User_a makes a channel
    channel_1 = http_channels_create(url, user_a["token"], "billionaire records", True).json()
    c_id_1 = channel_1["channel_id"]

    # User_a invites user_b
    http_channel_invite(url, user_a["token"], c_id_1, user_b["u_id"])

    # Retrieve user profiles
    user_a_profile = (http_user_profile(url, user_a["token"], user_a["u_id"]).json())["user"]
    user_b_profile = (http_user_profile(url, user_b["token"], user_b["u_id"]).json())["user"]

    # Check if user_b is inside the channel (channel_details)
    channel_details = http_channel_details(url, user_a["token"], c_id_1).json()

    assert channel_details == {
        "name": "billionaire records",
        "owner_members": [
            {
                "u_id": user_a["u_id"],
                "name_first": user_a_profile["name_first"],
                "name_last": user_a_profile["name_last"],
                "profile_img_url": user_a_profile["profile_img_url"],
            },
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


def test_channel_invite_http_success_2(url, user_a, user_b):
    """
    Test 2 - Check invited user is part of channel using channels_list
    """
    # User_a makes a channel
    channel_1 = http_channels_create(url, user_a["token"], "billionaire records", True).json()
    c_id_1 = channel_1["channel_id"]

    # User_a invites user_b
    http_channel_invite(url, user_a["token"], c_id_1, user_b["u_id"])

    # Check if user_b is inside the channel (channels_list)
    channel_list = http_channels_list(url, user_b["token"]).json()

    assert channel_list == {
        "channels": [
            {
                "channel_id": c_id_1,
                "name": "billionaire records",
            },
        ]
    }


def test_channel_invite_http_invalid_channel(url, user_a, user_b):
    """
    Test 3 - System Error - for invalid channel ID
    """
    # User_a cannot invite because channel_id is invalid
    invalid_cid = 4566343
    payload = http_channel_invite(url, user_a["token"], invalid_cid, user_b["u_id"])

    assert payload.status_code == 400


def test_channel_invite_http_invalid_user(url, user_a):
    """
    Test 4 - System Error - for invalid user ID
    """
    # User_a makes a channel
    channel_1 = http_channels_create(url, user_a["token"], "billionaire records", True).json()
    c_id_1 = channel_1["channel_id"]

    # User_a cannot invite because target u_id is invalid
    invalid_u_id = 4566343
    payload = http_channel_invite(url, user_a["token"], c_id_1, invalid_u_id)

    assert payload.status_code == 400


def test_channel_invite_access(url, user_a, user_b, user_c):
    """
    Test 5 - System Error - for user not being part of the channel
    """
    # User_a makes a channel
    channel_1 = http_channels_create(url, user_a["token"], "billionaire records", True).json()
    c_id_1 = channel_1["channel_id"]

    # User_b cannot invite user_c because user_b is not part of a channel
    payload = http_channel_invite(url, user_b["token"], c_id_1, user_c["u_id"])

    assert payload.status_code == 400


def test_channel_invite_http_invalid_token(url, user_a, user_b):
    """
    Test 6 - System Error - Invalid token passed in
    """
    # User_a makes a channel
    channel_1 = http_channels_create(url, user_a["token"], "billionaire records", True).json()
    c_id_1 = channel_1["channel_id"]

    # Error should be raised since token passed is invalid
    invalid_token = ""
    payload = http_channel_invite(url, invalid_token, c_id_1, user_b["u_id"])

    assert payload.status_code == 400
