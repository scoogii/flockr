"""
channel_removeowner_http_test

Testing that channel_addowner works with
http implementation
"""


import requests
from echo_http_test import url
from conftest_http import user_a, user_b, user_c
from http_channel_functions import (
    http_channel_details,
    http_channel_addowner,
    http_channel_removeowner,
    http_channel_join,
)
from http_channels_functions import http_channels_create
from http_user_functions import http_user_profile



def test_channel_removeowner_success(url, user_a, user_b):
    """
    Test 1 - Channel removeowner successfully removes another channel owner
    """
    # User_a makes a channel
    channel_1 = http_channels_create(url, user_a["token"], "billionaire records", True).json()
    c_id_1 = channel_1["channel_id"]

    # User_b joins the channel
    http_channel_join(url, user_b["token"], c_id_1)

    # User_a makes User_b the channel owner
    http_channel_addowner(url, user_a["token"], c_id_1, user_b["u_id"])

    # User_b removes User_a the channel owner
    http_channel_removeowner(url, user_b["token"], c_id_1, user_a["u_id"])

    # Retrieve user_profiles
    user_a_profile = (http_user_profile(url, user_a["token"], user_a["u_id"]).json())["user"]
    user_b_profile = (http_user_profile(url, user_b["token"], user_b["u_id"]).json())["user"]

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


def test_channel_removeowner_admin_success(url, user_a, user_b):
    """
    Test 2 - Channel removeowner successfully removes another member as channel owner
    based on admin permission rights
    """
    # User_b makes a channel
    channel_1 = http_channels_create(url, user_b["token"], "billionaire records", True).json()
    c_id_1 = channel_1["channel_id"]

    # User_a joins the channel
    http_channel_join(url, user_a["token"], c_id_1)

    # User_a removes User_b since user_a is the admin of flockr
    http_channel_removeowner(url, user_a["token"], c_id_1, user_b["u_id"])

    # Retrieve user_profiles
    user_a_profile = (http_user_profile(url, user_a["token"], user_a["u_id"]).json())["user"]
    user_b_profile = (http_user_profile(url, user_b["token"], user_b["u_id"]).json())["user"]

    channel_details = http_channel_details(url, user_a["token"], c_id_1).json()

    assert channel_details == {
        "name": "billionaire records",
        "owner_members": [],
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
        ],
    }


def test_channel_removeowner_invalid(url, user_a, user_b):
    """
    Test 3 - Channel removeowner raises an error
    based on invalid Channel ID
    """
    # User_a makes a channel
    channel_1 = http_channels_create(url, user_a["token"], "billionaire records", True).json()
    c_id_1 = channel_1["channel_id"]

    # User_b joins the channel
    http_channel_join(url, user_b["token"], c_id_1)

    # User_a cannot remove owner based on invalid Channel ID
    invalid_cid = 12345
    payload = http_channel_removeowner(url, user_a["token"], invalid_cid, user_b["u_id"])

    assert payload.status_code == 400


def test_channel_removeowner_unauth(url, user_a, user_b, user_c):
    """
    Test 4 - Channel removeowner raises an error
    based on User ID not being the owner
    """
    # User_a makes a channel
    channel_1 = http_channels_create(url, user_a["token"], "billionaire records", True).json()
    c_id_1 = channel_1["channel_id"]

    # User_b joins the channel
    http_channel_join(url, user_b["token"], c_id_1)

    # User_c joins the channel
    http_channel_join(url, user_c["token"], c_id_1)

    # User_b cannot remove owner based on not being an owner
    payload = http_channel_removeowner(url, user_b["token"], c_id_1, user_c["u_id"])

    assert payload.status_code == 400


def test_channel_uid_not_owner(url, user_a, user_b):
    """
    Test 5 - Channel removeowner raises an error
    based on User ID not being the owner
    """
    # User_a makes a channel
    channel_1 = http_channels_create(url, user_a["token"], "billionaire records", True).json()
    c_id_1 = channel_1["channel_id"]

    # User_b joins the channel
    http_channel_join(url, user_b["token"], c_id_1)

    # User_a cannot remove owner because user_b is not an owner
    payload = http_channel_removeowner(url, user_a["token"], c_id_1, user_b["u_id"])

    assert payload.status_code == 400


def test_channel_removeowner_invalid_token(url, user_a, user_b):
    """
    Test 6 - Channel removeowner raises error based on invalid token
    """
    # User_a makes a channel
    channel_1 = http_channels_create(url, user_a["token"], "billionaire records", True).json()
    c_id_1 = channel_1["channel_id"]

    # User_b joins the channel
    http_channel_join(url, user_b["token"], c_id_1)

    # User_a makes user_b owner
    http_channel_addowner(url, user_a["token"], c_id_1, user_b["u_id"])

    # User_a cannot remove user_b as owner because invalid token is passed
    invalid_token = 12345
    payload = http_channel_removeowner(url, invalid_token, c_id_1, user_b["u_id"])

    assert payload.status_code == 400
