"""
channel_join

Takes in (token, channel_id)
Returns {}

Description: Given a channel_id of a channel that the authorised user can join,
adds them to that channel

Exceptions:
- InputError when any of Channel ID is not a valid channel
- AccessError when channel_id refers to a channel that is private
(when the authorised user is not an admin)
"""


import pytest
from auth import auth_register
from channel import channel_join, channel_details
from channels import channels_create, channels_list
from error import InputError, AccessError
from other import clear
from user import user_profile
from conftest import user_a, user_b


def test_channel_join_success_1(user_a, user_b):
    """
    Test 1 - Testing user that joined is added to channel using channel_details
    """
    # User_a makes a channel
    channel_1 = channels_create(user_a["token"], "billionaire records", True)
    c_id_1 = channel_1["channel_id"]

    # User_b joins the channel
    channel_join(user_b["token"], c_id_1)

    token = user_b["token"]

    user_a = (user_profile(user_a["token"], user_a["u_id"]))["user"]
    user_b = (user_profile(user_b["token"], user_b["u_id"]))["user"]


    # Check if the person is inside the channel (channel_detail)
    assert channel_details(token, c_id_1) == {
        "name": "billionaire records",
        "owner_members": [
            {
                "u_id": user_a["u_id"],
                "name_first": user_a["name_first"],
                "name_last": user_a["name_last"],
                "profile_img_url": user_a["profile_img_url"],
            }
        ],
        "all_members": [
            {
                "u_id": user_a["u_id"],
                "name_first": user_a["name_first"],
                "name_last": user_a["name_last"],
                "profile_img_url": user_a["profile_img_url"],
            },
            {
                "u_id": user_b["u_id"],
                "name_first": user_b["name_first"],
                "name_last": user_b["name_last"],
                "profile_img_url": user_b["profile_img_url"],
            },
        ],
    }

    clear()


def test_channel_join_success_2(user_a, user_b):
    """
    Test 2 - Testing user that joined is added to channel using channels_list
    """
    # User_a makes a channel
    channel_1 = channels_create(user_a["token"], "billionaire records", True)
    c_id_1 = channel_1["channel_id"]

    # User_b joins the channel
    channel_join(user_b["token"], c_id_1)

    # Check if the person is inside the channel (channels_list)
    assert channels_list(user_b["token"]) == {
        "channels": [
            {
                "channel_id": c_id_1,
                "name": "billionaire records",
            }
        ],
    }

    clear()


def test_channel_join_invalid(user_a):
    """
    Test 3 - InputError - for invalid channel ID
    """
    # Create an invalid channel_id
    invalid_c_id = 4566343

    # User_a cannot join because channel_id is invalid
    with pytest.raises(InputError):
        channel_join(user_a["token"], invalid_c_id)

    clear()


def test_channel_join_private(user_a, user_b):
    """
    Test 4 - AccessError - for when user is not authorised to join channel
    """
    # User_a makes a channel
    channel_1 = channels_create(user_a["token"], "the cage", False)
    c_id_1 = channel_1["channel_id"]

    # User_b cannot join because it is private
    with pytest.raises(AccessError, match=r"User is not authorised to join channel"):
        channel_join(user_b["token"], c_id_1)

    clear()


def test_channel_join_invalid_token(user_a):
    """
    Test 5 - AccessError - Invalid token passed in
    """
    # User_a makes a channel
    channel_1 = channels_create(user_a["token"], "billionaire records", True)
    c_id_1 = channel_1["channel_id"]
    invalid_token = ""

    # Cannot check because an invalid token was passed in
    with pytest.raises(AccessError, match=r"Invalid Token"):
        channel_join(invalid_token, c_id_1)

    clear()
