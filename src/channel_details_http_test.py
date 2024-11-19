"""
channel_details_http_test

Testing that channel_details works with
http implementation
"""


import requests
from echo_http_test import url
from conftest_http import user_a, user_b
from http_channel_functions import (
    http_channel_details,
    http_channel_addowner,
    http_channel_removeowner,
    http_channel_join,
)
from http_channels_functions import http_channels_create
from http_user_functions import http_user_profile


def test_channel_detail_http_success(url, user_a, user_b):
    """
    Test 1 - Channel details request successfuly returns correct data
    Anything with user_a accesses the name, email and password
    Anything that is user_a accsses the u_id and token
    """
    # User_a makes a channel
    channel_1 = http_channels_create(url, user_a["token"], "billionaire records", True).json()
    c_id_1 = channel_1["channel_id"]

    # User_b joins the channel
    http_channel_join(url, user_b["token"], c_id_1)

    # Retrieve user_profile for each user
    user_a_profile = (http_user_profile(url, user_a["token"], user_a["u_id"]).json())["user"]
    user_b_profile = (http_user_profile(url, user_b["token"], user_b["u_id"]).json())["user"]

    # Check if user_b is inside the channel
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
                "profile_img_url": user_b_profile["profile_img_url"]
            },
        ],
    }


def test_channel_detail_http_invalid_channel(url, user_a):
    """
    Test 2 - System Error - Invalid Channel ID
    """
    # User_a cannot receive channel details because channel_id is invalid
    invalid_cid = 4566343
    payload = http_channel_details(url, user_a["token"], invalid_cid)
    assert payload.status_code == 400


def test_channel_detail_http_unauth_user(url, user_a, user_b):
    """
    Test 3 - System Error - For when user is not part of the channel
    """
    # User_a makes the channel
    channel_1 = http_channels_create(url, user_a["token"], "billionaire records", True).json()
    c_id_1 = channel_1["channel_id"]

    # User_b cannot request channel details because they are not apart of the channel
    payload = http_channel_details(url, user_b["token"], c_id_1)
    assert payload.status_code == 400


def test_channel_detail_http_invalid_token(url, user_a):
    """
    Test 4 - System Error = Invalid token passed in
    """
    # User_a makes the channel
    c_id_1 = http_channels_create(url, user_a["token"], "billionaire records", True)

    # Channel details cannot be returned due to invalid token
    invalid_token = ""
    payload = http_channel_details(url, invalid_token, c_id_1)
    assert payload.status_code == 500
