"""
channel_details

Takes in (token, channel_id)
Returns { name, owner_members, all_members }

Description: Given a Channel with ID channel_id that the authorised user
is part of, provide basic details about the channel

Exceptions:
- InputError when any of: Channel ID is not a valid channel
- AccessError when Authorised user is not a member of channel with channel_id
"""


import pytest
from channel import channel_join, channel_details
from channels import channels_create
from error import InputError, AccessError
from other import clear
from user import user_profile
from conftest import user_a, user_b, user_c


def test_channel_detail_success(user_a, user_b):
    """
    Test 1 - Channel details successfully returns correct data
    Anything with user_a accesses the name, email and password
    Anything that is user_a accsses the u_id and token
    """
    # User_a makes a channel
    channel_1 = channels_create(user_a["token"], "billionaire records", True)
    c_id_1 = channel_1["channel_id"]

    # User_b joins the channel
    channel_join(user_b["token"], c_id_1)

    token = user_a["token"]

    user_a = (user_profile(user_a["token"], user_a["u_id"]))["user"]
    user_b = (user_profile(user_b["token"], user_b["u_id"]))["user"]

    # Check the channel details
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


def test_channel_detail_invalid_channel(user_a):
    """
    Test 2 - InputError - for invalid channel ID
    """
    # Create an invalid channel_id
    invalid_c_id = 4566343

    # User_a cannot check details because channel id is invalid
    with pytest.raises(InputError):
        channel_details(user_a["token"], invalid_c_id)

    clear()


def test_channel_detail_unauth_user(user_a, user_b):
    """
    Test 3 - AccessError - for when user is not part of the channel
    """
    # User_a makes a channel
    channel_1 = channels_create(user_a["token"], "billionaire records", True)
    c_id_1 = channel_1["channel_id"]

    # User_b cannot check because user_b isn't a part of the channel
    with pytest.raises(AccessError, match=r"You must be a member of the channel to view its details"):
        channel_details(user_b["token"], c_id_1)

    clear()


def test_channel_detail_invalid_token(user_a):
    """
    Test 4 - AccessError - Invalid token passed in
    """
    # User_a makes a channel
    channel_1 = channels_create(user_a["token"], "billionaire records", True)
    c_id_1 = channel_1["channel_id"]
    invalid_token = ""

    # AccessError should be raised since token passed is invalid
    with pytest.raises(AccessError, match=r"Invalid Token"):
        channel_details(invalid_token, c_id_1)

    clear()
