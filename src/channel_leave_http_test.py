"""
channel_leave_http_test

Testing that channel_leave works with
http implementation
"""


import requests
from echo_http_test import url
from conftest_http import user_a, user_b
from http_channel_functions import (
    http_channel_details,
    http_channel_join,
    http_channel_leave,
)
from http_channels_functions import http_channels_create, http_channels_list
from http_user_functions import http_user_profile


def test_channel_leave_http_success_1(url, user_a, user_b):
    """
    Test 1 - Testing that user leaves channel successfully using channel_details
    """
    # User_a makes a channel
    channel_1 = http_channels_create(url, user_a["token"], "billionaire records", True).json()
    c_id_1 = channel_1["channel_id"]

    # User_b joins the channel
    http_channel_join(url, user_b["token"], c_id_1)

    # User_b decides to leave the channel
    http_channel_leave(url, user_b["token"], c_id_1)

    # Retrieve user profiles
    user_a_profile = (http_user_profile(url, user_a["token"], user_a["u_id"]).json())["user"]

    # Check that the user has left by checking channel_details
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
        ],
    }


def test_channel_leave_http_success_2(url, user_a, user_b):
    """
    Test 2 - Testing that user leaves channel successfully using channels_list
    """
    # User_a makes a channel
    channel_1 = http_channels_create(url, user_a["token"], "billionaire records", True).json()
    c_id_1 = channel_1["channel_id"]

    # User_b joins the channel
    http_channel_join(url, user_b["token"], c_id_1)

    # User_b decides to leave the channel
    http_channel_leave(url, user_b["token"], c_id_1)

    # Check that the user has left by checking channels_list
    channel_list = http_channels_list(url, user_b["token"]).json()

    assert channel_list == {"channels": []}


def test_channel_leave_http_invalid_channel(url, user_a):
    """
    Test 3 - System Error - for invalid channel ID
    """
    # User_b cannot leave because id is invalid
    invalid_cid = 4566343
    payload = http_channel_leave(url, user_a["token"], invalid_cid)

    assert payload.status_code == 400


def test_channel_leave_http_not_part_of_channel(url, user_a, user_b):
    """
    Test 4 - System Error - for when user is not part of the channel
    """
    # User_a makes a channel
    channel_1 = http_channels_create(url, user_a["token"], "billionaire records", True).json()
    c_id_1 = channel_1["channel_id"]

    # User_b cannot leave because they were never a part of the channel
    payload = http_channel_leave(url, user_b["token"], c_id_1)

    assert payload.status_code == 400


def test_channel_leave_http_invalid_token(url, user_a):
    """
    Test 5 - System Error - Invalid token passed in
    """
    # User_a makes a channel
    channel_1 = http_channels_create(url, user_a["token"], "billionaire records", True).json()
    c_id_1 = channel_1["channel_id"]

    # Error should be raised since token is invalid
    invalid_token = ""
    payload = http_channel_leave(url, invalid_token, c_id_1)

    assert payload.status_code == 400
