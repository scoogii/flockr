"""
channel_leave

Takes in (token, channel_id)
Returns {}

Description: Given a channel ID, the user removed as a member of this channel

Exceptions:
- InputError when any of Channel ID is not a valid channel
- AccessError when Authorised user is not a member of channel with channel_id
"""


import pytest
from auth import auth_register
from channel import channel_join, channel_details, channel_leave
from channels import channels_create, channels_list
from error import InputError, AccessError
from other import clear
from user import user_profile
from conftest import user_a, user_b, user_c


def test_channel_leave_success_1(user_a, user_b):
    """
    Test 1.1 - Testing that user leaves channel successfully using channel_details
    """
    # User_a makes a channel
    channel_1 = channels_create(user_a["token"], "billionaire records", True)
    c_id_1 = channel_1["channel_id"]

    # User_b joins the channel
    channel_join(user_b["token"], c_id_1)

    # User_b decides to leave the channel
    channel_leave(user_b["token"], c_id_1)

    token = user_a["token"]

    user_a = (user_profile(user_a["token"], user_a["u_id"]))["user"]

    # Assert the user has left by checking channel_details
    assert channel_details(token, c_id_1) == {
        "name": "billionaire records",
        "owner_members": [
            {
                "u_id": user_a["u_id"],
                "name_first": user_a["name_first"],
                "name_last": user_a["name_last"],
                "profile_img_url": user_a["profile_img_url"],
            },
        ],
        "all_members": [
            {
                "u_id": user_a["u_id"],
                "name_first": user_a["name_first"],
                "name_last": user_a["name_last"],
                "profile_img_url": user_a["profile_img_url"],
            },
        ],
    }

    clear()


def test_channel_leave_success_2(user_a, user_b):
    """
    Test 1.2 - Testing that user leaves channel successfully using channels_list
    """
    # User_a makes a channel
    channel_1 = channels_create(user_a["token"], "billionaire records", True)
    c_id_1 = channel_1["channel_id"]

    # User_b joins the channel
    channel_join(user_b["token"], c_id_1)

    # User_b decides to leave the channel
    channel_leave(user_b["token"], c_id_1)

    # Check if the person is not inside the channel (channels_list)
    assert channels_list(user_b["token"]) == {"channels": []}

    clear()


def test_channel_all_leave(user_a, user_b, user_c):
    """
    Test 2 - Testing that user leaves channel successfully using channels_list
    """
    # User_a makes a channel
    channel_1 = channels_create(user_a["token"], "billionaire records", True)
    c_id_1 = channel_1["channel_id"]

    # User_b and user_c join the channel
    channel_join(user_b["token"], c_id_1)
    channel_join(user_c["token"], c_id_1)

    # All users leave the channel
    channel_leave(user_a["token"], c_id_1)
    channel_leave(user_b["token"], c_id_1)
    channel_leave(user_c["token"], c_id_1)

    # user_a rejoins the channel 
    channel_join(user_a["token"], c_id_1)

    token = user_a["token"]

    user_a = (user_profile(user_a["token"], user_a["u_id"]))["user"]
    
    # user_a checks the channel details
    assert channel_details(token, c_id_1) == {
        "name": "billionaire records",
        "owner_members": [],
        "all_members": [
            {
                "u_id": user_a["u_id"],
                "name_first": user_a["name_first"],
                "name_last": user_a["name_last"],
                "profile_img_url": user_a["profile_img_url"],
            },
        ],
    }

    clear()


def test_channel_leave_invalid_channel(user_a):
    """
    Test 3 - InputError - for invalid channel ID
    """
    # Create an invalid channel_id
    invalid_c_id = 4566343

    # User_b cannot leave because id is invalid
    with pytest.raises(InputError):
        channel_leave(user_a["token"], invalid_c_id)

    clear()


def test_channel_leave_not_part_of_channel(user_a, user_b):
    """
    Test 4 - AccessError - for when user is not part of the channel
    """
    # User_a makes a channel
    channel_1 = channels_create(user_a["token"], "billionaire records", True)
    c_id_1 = channel_1["channel_id"]

    # User_b cannot leave because user 2 isn't a part of the channel
    with pytest.raises(AccessError, match=r"You must be a member of the channel to view its details"):
        channel_leave(user_b["token"], c_id_1)

    clear()


def test_channel_leave_invalid_token(user_a):
    """
    Test 5 - AccessError - Invalid token passed in
    """
    # User_a makes a channel
    channel_1 = channels_create(user_a["token"], "billionaire records", True)
    c_id_1 = channel_1["channel_id"]
    invalid_token = ""

    # No user can leave because the token doesn't exist
    with pytest.raises(AccessError, match=r"Invalid Token"):
        channel_leave(invalid_token, c_id_1)

    clear()
