"""
channel_invite

Takes in (token, channel_id, u_id)
Returns {}

Description: Invites a user (with user id u_id) to join a channel with ID
channel_id. Once invited the user is added to the channel immediately

Exceptions:
- InputError when any of:
    - channel_id does not refer to a valid channel that the authorised user is
    part of
    - u_id does not refer to a valid user
- AccessError whenthe authorised user is not already a member of the channel
"""


import pytest
from auth import auth_register
from channel import channel_invite, channel_details
from channels import channels_create, channels_list
from error import InputError, AccessError
from other import clear
from user import user_profile
from conftest import user_a, user_b, user_c


def test_channel_invite_success_1(user_a, user_b):
    """
    Test 1 - Channel invite successfully adds another user to channel
    """
    # User_a makes a channel
    channel_1 = channels_create(user_a["token"], "billionaire records", True)
    c_id_1 = channel_1["channel_id"]

    # User_a invites second user
    channel_invite(user_a["token"], c_id_1, user_b["u_id"])

    token = user_b["token"]

    user_a = (user_profile(user_a["token"], user_a["u_id"]))["user"]
    user_b = (user_profile(user_b["token"], user_b["u_id"]))["user"]

    # Check if User_b is inside the channel (channel_detail)
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
            {
                "u_id": user_b["u_id"],
                "name_first": user_b["name_first"],
                "name_last": user_b["name_last"],
                "profile_img_url": user_b["profile_img_url"],
            },
        ],
    }

    clear()


def test_channel_invite_success_2(user_a, user_b):
    """
    Test 2 - Checking invited user is part of channel using channels_list
    """
    # User_a makes a channel
    channel_1 = channels_create(user_a["token"], "billionaire records", True)
    c_id_1 = channel_1["channel_id"]

    # User_a invites second user
    channel_invite(user_a["token"], c_id_1, user_b["u_id"])

    # Check if User_b is inside the channel (channels_list) by inputting user_b's token
    assert channels_list(user_b["token"]) == {
        "channels": [
            {
                "channel_id": c_id_1,
                "name": "billionaire records",
            }
        ],
    }

    clear()


def test_channel_invite_invalid_channel(user_a, user_b):
    """
    Test 3 - InputError - for invalid channel ID
    """
    # User_a cannot invite because c_id is invalid
    with pytest.raises(InputError):
        # Create invalid channel_id
        invalid_c_id = 4566343
        channel_invite(user_a["token"], invalid_c_id, user_b["u_id"])

    clear()


def test_channel_invite_invalid_user(user_a):
    """
    Test 4 - InputError - for invalid user ID
    """
    # User_a cannot invite because u_id is invalid
    with pytest.raises(InputError, match=r"Invalid User ID"):
        # User_a makes a channel
        channel_1 = channels_create(user_a["token"], "billionaire records", True)
        c_id_1 = channel_1["channel_id"]

        invalid_u_id = 4566343
        channel_invite(user_a["token"], c_id_1, invalid_u_id)

    clear()


def test_channel_invite_invalid_access(user_a, user_b, user_c):
    """
    Test 5 - AccessError - for user not being part of a channel
    """
    # User_b cannot invite User_c because User_b is not part of a channel
    with pytest.raises(AccessError, match=r"You must be a member of the channel to view its details"):
        # User_a makes a channel
        channel_1 = channels_create(user_a["token"], "billionaire records", True)
        c_id_1 = channel_1["channel_id"]

        channel_invite(user_b["token"], c_id_1, user_c["u_id"])

    clear()


def test_channel_invite_invalid_token(user_a, user_b):
    """
    Test 6 - AccessError - Invalid token passed in
    """
    # User_a makes a channel
    channel_1 = channels_create(user_a["token"], "billionaire records", True)
    c_id_1 = channel_1["channel_id"]
    invalid_token = ""

    # AccessError should be raised since token passed is invalid
    with pytest.raises(AccessError, match=r"Invalid Token"):
        channel_invite(invalid_token, c_id_1, user_b["u_id"])

    clear()


def test_channel_invite_u_id_already_member(user_a, user_b):
    """
    Test 7 - InputError - user with u_id is already a member
    """
    # User_a makes a channel
    channel_1 = channels_create(user_a["token"], "billionaire records", True)
    c_id_1 = channel_1["channel_id"]

    # User_b is added to the channel
    channel_invite(user_a["token"], c_id_1, user_b["u_id"])

    # InputError should be raised since user_b has already become a part of the channel
    with pytest.raises(InputError, match=r"User already a member of this channel"):
        channel_invite(user_a["token"], c_id_1, user_b["u_id"])

    clear()
