"""
channel_removemember_http_test

Testing that channel_removemember works with
http implementation
"""


import requests
from echo_http_test import url
from conftest_http import user_a, user_b, user_c
from http_channel_functions import (
    http_channel_details,
    http_channel_join,
    http_channel_removeowner,
    http_channel_removemember,
)
from http_channels_functions import http_channels_create
from http_user_functions import http_user_profile


def test_channel_removemember_http_success_owner(url, user_a, user_b):
    """
    Test 1 - Tests that a channel owner can successfully remove
    a member from the channel
    """
    # User_a makes a channel
    channel_1 = http_channels_create(url, user_a["token"], "billionaire records", True).json()
    c_id_1 = channel_1["channel_id"]

    # User_b joins the channel
    http_channel_join(url, user_b["token"], c_id_1)

    # User_a removes user_b as a member
    http_channel_removemember(url, user_a["token"], c_id_1, user_b["u_id"])

    # Get the profile for user_a
    user_a_profile = (http_user_profile(url, user_a["token"], user_a["u_id"]).json())["user"]

    # Check that user_b was succesfully removed from channel_1
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


def test_channel_removemember_http_success_admin(url, user_a, user_b):
    """
    Test 2 - Tests that an admin can successfully remove a member
    from the channel
    """
    # User_b makes a channel
    channel_1 = http_channels_create(url, user_b["token"], "billionaire records", True).json()
    c_id_1 = channel_1["channel_id"]

    # User_a joins the channel
    http_channel_join(url, user_a["token"], c_id_1)

    # User_a removes user_b as a channel owner
    http_channel_removeowner(url, user_a["token"], c_id_1, user_b["u_id"])

    # User_a removes user_b as a member
    http_channel_removemember(url, user_a["token"], c_id_1, user_b["u_id"])

    # Get the profile for user_a
    user_a_profile = (http_user_profile(url, user_a["token"], user_a["u_id"]).json())["user"]

    # Check that user_b was succesfully removed from channel_1
    channel_details = http_channel_details(url, user_a["token"], c_id_1).json()

    assert channel_details == {
        "name": "billionaire records",
        "owner_members": [],
        "all_members": [
            {
                "u_id": user_a["u_id"],
                "name_first": user_a_profile["name_first"],
                "name_last": user_a_profile["name_last"],
                "profile_img_url": user_a_profile["profile_img_url"],
            },
        ],
    }


def test_channel_removemember_http_success_remove_owner(url, user_a, user_b):
    """
    Test 3 - Tests that an admin can succesfully remove an owner
    from the channel
    """
    # User_b makes a channel
    channel_1 = http_channels_create(url, user_b["token"], "billionaire records", True).json()
    c_id_1 = channel_1["channel_id"]

    # User_a joins the channel
    http_channel_join(url, user_a["token"], c_id_1)

    # User_a removes user_b as a member and owner
    http_channel_removemember(url, user_a["token"], c_id_1, user_b["u_id"])

    # Get the profile for user_a
    user_a_profile = (http_user_profile(url, user_a["token"], user_a["u_id"]).json())["user"]

    # Check that user_b was succesfully removed from channel_1
    channel_details = http_channel_details(url, user_a["token"], c_id_1).json()

    assert channel_details == {
        "name": "billionaire records",
        "owner_members": [],
        "all_members": [
            {
                "u_id": user_a["u_id"],
                "name_first": user_a_profile["name_first"],
                "name_last": user_a_profile["name_last"],
                "profile_img_url": user_a_profile["profile_img_url"],
            },
        ],
    }


def test_channel_removemember_http_invalid_uid(url, user_a):
    """
    Test 4 - System Error - Invalid u_id
    """
    # User_a makes a channel
    channel_1 = http_channels_create(url, user_a["token"], "billionaire records", True).json()
    c_id_1 = channel_1["channel_id"]

    # Error should be raised since u_id is invalid
    invalid_uid = 696969
    payload = http_channel_removemember(url, user_a["token"], c_id_1, invalid_uid)
    assert payload.status_code == 400


def test_channel_removemember_http_invalid_cid(url, user_a, user_b):
    """
    Test 5 - System Error - Invalid channel ID
    """
    # Error should be raised since channel ID is invalid
    invalid_cid = 696969
    payload = http_channel_removemember(url, user_a["token"], invalid_cid, user_b["u_id"])

    assert payload.status_code == 400


def test_channel_removemember_http_self(url, user_a):
    """
    Test 6 - System Error - User attempts to remove themselves from channel
    """
    # User_a makes a channel
    channel_1 = http_channels_create(url, user_a["token"], "billionaire records", True).json()
    c_id_1 = channel_1["channel_id"]

    # Error should be raised since user cannot remove themselves from channel
    payload = http_channel_removemember(url, user_a["token"], c_id_1, user_a["u_id"])

    assert payload.status_code == 400


def test_channel_removemember_http_unauth(url, user_a, user_b):
    """
    Test 7 - System Error - User attempting to remove another
    user is not an admin of the flockr, or an owner of the
    channel
    """
    # User_b makes a channel
    channel_1 = http_channels_create(url, user_b["token"], "billionaire records", True).json()
    c_id_1 = channel_1["channel_id"]

    # User_a joins the channel
    http_channel_join(url, user_a["token"], c_id_1)

    # User_a removes user_b as an owner
    http_channel_removeowner(url, user_a["token"], c_id_1, user_b["u_id"])

    # Error should be raised since user_b is not authorised to remove members
    payload = http_channel_removemember(url, user_b["token"], c_id_1, user_a["u_id"])

    assert payload.status_code == 400


def test_channel_removemember_http_invalid_token(url, user_a):
    """
    Test 8 - System Error - Invalid token
    """
    # User_a makes a channel
    channel_1 = http_channels_create(url, user_a["token"], "billionaire records", True).json()
    c_id_1 = channel_1["channel_id"]

    # Error should be raised since the token passed in is invalid
    invalid_token = ""
    payload = http_channel_removemember(url, invalid_token, c_id_1, user_a["u_id"])

    assert payload.status_code == 400
