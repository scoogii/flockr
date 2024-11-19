"""
channel_addowner_http_test.py

Testing that channel_addowner works with
http implementation
"""


import requests
from echo_http_test import url
from conftest_http import user_a, user_b, user_c
from http_channels_functions import http_channels_create
from http_channel_functions import (
    http_channel_addowner,
    http_channel_details,
    http_channel_join,
)
from http_user_functions import http_user_profile


def test_channel_addowner_success(url, user_a, user_b):
    """
    Test 1 - Channel addowner successfully adds another member as a channel owner
    """
    # User_a makes a channel
    channel_1 = http_channels_create(url, user_a["token"], "billionaire records", True).json()
    c_id_1 = channel_1["channel_id"]

    # User_b joins the channel
    http_channel_join(url, user_b["token"], c_id_1)

    # User_a makes User_b the channel owner
    http_channel_addowner(url, user_a["token"], c_id_1, user_b["u_id"])

    # Retrieve user_profile for each user
    user_a_info = (http_user_profile(url, user_a["token"], user_a["u_id"]).json())["user"]
    user_b_info = (http_user_profile(url, user_b["token"], user_b["u_id"]).json())["user"]

    channel_details = http_channel_details(url, user_a["token"], c_id_1).json()

    assert channel_details == {
        "name": "billionaire records",
        "owner_members": [
            {
                "u_id": user_a["u_id"],
                "name_first": user_a_info["name_first"],
                "name_last": user_a_info["name_last"],
                "profile_img_url": user_a_info["profile_img_url"],
            },
            {
                "u_id": user_b["u_id"],
                "name_first": user_b_info["name_first"],
                "name_last": user_b_info["name_last"],
                "profile_img_url": user_b_info["profile_img_url"],
            },
        ],
        "all_members": [
            {
                "u_id": user_a["u_id"],
                "name_first": user_a_info["name_first"],
                "name_last": user_a_info["name_last"],
                "profile_img_url": user_a_info["profile_img_url"],
            },
            {
                "u_id": user_b["u_id"],
                "name_first": user_b_info["name_first"],
                "name_last": user_b_info["name_last"],
                "profile_img_url": user_b_info["profile_img_url"],
            },
        ],
    }


def test_admin_permission_success(url, user_a, user_b, user_c):
    """
    Test 2 - Channel addowner successfully adds another user as owner
    based on admin permission rights
    """
    # User_b makes a channel
    channel_1 = http_channels_create(url, user_b["token"], "billionaire records", True).json()
    c_id_1 = channel_1["channel_id"]

    # User_a who is an admin joins the channel
    http_channel_join(url, user_a["token"], c_id_1)

    # User_c joins the channel
    http_channel_join(url, user_c["token"], c_id_1)

    # User_a makes user_c the channel owner
    http_channel_addowner(url, user_a["token"], c_id_1, user_c["u_id"])

    # Retrieve user_profile for each user
    user_a_profile = (http_user_profile(url, user_a["token"], user_a["u_id"]).json())["user"]
    user_b_profile = (http_user_profile(url, user_b["token"], user_b["u_id"]).json())["user"]
    user_c_profile = (http_user_profile(url, user_c["token"], user_c["u_id"]).json())["user"]

    channel_details = http_channel_details(url, user_a["token"], c_id_1).json()

    assert channel_details == {
        "name": "billionaire records",
        "owner_members": [
            {
                "u_id": user_b["u_id"],
                "name_first": user_b_profile["name_first"],
                "name_last": user_b_profile["name_last"],
                "profile_img_url": user_b_profile["profile_img_url"],
            },
            {
                "u_id": user_c["u_id"],
                "name_first": user_c_profile["name_first"],
                "name_last": user_c_profile["name_last"],
                "profile_img_url": user_c_profile["profile_img_url"],
            },
        ],
        "all_members": [
            {
                "u_id": user_b["u_id"],
                "name_first": user_b_profile["name_first"],
                "name_last": user_b_profile["name_last"],
                "profile_img_url": user_b_profile["profile_img_url"],
            },
            {
                "u_id": user_a["u_id"],
                "name_first": user_a_profile["name_first"],
                "name_last": user_a_profile["name_last"],
                "profile_img_url": user_a_profile["profile_img_url"],
            },
            {
                "u_id": user_c["u_id"],
                "name_first": user_c_profile["name_first"],
                "name_last": user_c_profile["name_last"],
                "profile_img_url": user_c_profile["profile_img_url"],
            },
        ],
    }


def test_channel_addowner_already(url, user_a, user_b):
    """
    Test 3 - Channel addowner raises an error
    based on user already being an owner
    """
    # User_a makes a channel
    channel_1 = http_channels_create(url, user_a["token"], "billionaire records", True).json()
    c_id_1 = channel_1["channel_id"]

    # User_b joins the channel
    http_channel_join(url, user_b["token"], c_id_1)

    # User_a makes User_b a channel owner
    http_channel_addowner(url, user_a["token"], c_id_1, user_b["u_id"])

    # User_a cannot add user_b as an owner because user_b is already an owner
    payload = http_channel_addowner(url, user_a["token"], c_id_1, user_b["u_id"])

    assert payload.status_code == 400


def test_channel_addowner_unauth(url, user_a, user_b, user_c):
    """
    Test 4 - Channel addowner raises an error
    based on user not being the owner
    """
    # User_a makes a channel
    channel_1 = http_channels_create(url, user_a["token"], "billionaire records", True).json()
    c_id_1 = channel_1["channel_id"]

    # User_b joins the channel
    http_channel_join(url, user_b["token"], c_id_1)

    # User_c joins the channel
    http_channel_join(url, user_c["token"], c_id_1)

    # User_c cannot add user_b as owner because they are not owner
    payload = http_channel_addowner(url, user_c["token"], c_id_1, user_b["u_id"])

    assert payload.status_code == 400


def test_channel_addowner_invalid_token(url, user_a, user_b):
    """
    Test 5 - Channel addowner raises error based on invalid token
    """
    # User_a makes a channel
    channel_1 = http_channels_create(url, user_a["token"], "billionaire records", True).json()
    c_id_1 = channel_1["channel_id"]

    # User_b joins the channel
    http_channel_join(url, user_b["token"], c_id_1)

    # Invalid token passed in
    invalid_token = 12345
    payload = http_channel_addowner(url, invalid_token, c_id_1, user_b["u_id"])

    assert payload.status_code == 400
