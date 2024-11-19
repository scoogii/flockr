"""
channel_removemember

Takes in (token, channel_id, u_id)
Returns {}

Description: Remove user with user id u_id as a member of this channel

Exceptions:
- InputError when any of:
  - Channel ID is not a valid channel
  - Invalid u_id (not part of the channel or doesn't exist)
  - User attempts to remove themselves from channel
- AccessError when any of:
  - Authorised user is not an admin of the flockr, or an owner
  of this channel
  - Invalid token
"""


import pytest
from channel import (
    channel_details,
    channel_join,
    channel_removemember,
    channel_removeowner
)
from channels import channels_create
from error import InputError, AccessError
from other import clear
from user import user_profile
from conftest import user_a, user_b


def test_channel_removemember_success_owner(user_a, user_b):
    """
    Test 1 - Tests that a channel owner can successfully remove
    a member from the channel
    """
    # User_a makes a channel
    channel_1 = channels_create(user_a["token"], "billionaire records", True)
    c_id_1 = channel_1["channel_id"]

    # User_b joins the channel
    channel_join(user_b["token"], c_id_1)

    # User_a removes user_b as a member
    channel_removemember(user_a["token"], c_id_1, user_b["u_id"])

    user_a_profile = (user_profile(user_a["token"], user_a["u_id"]))["user"]

    # Check that user_b was successfully removed from channel_1
    assert channel_details(user_a["token"], c_id_1) == {
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

    clear()


def test_channel_removemember_success_admin(user_a, user_b):
    """
    Test 2 - Tests that an admin can successfully remove a member
    from the channel
    """
    # User_b makes a channel
    channel_1 = channels_create(user_b["token"], "billionaire records", True)
    c_id_1 = channel_1["channel_id"]

    # User_a (admin of Flockr) joins the channel
    channel_join(user_a["token"], c_id_1)

    # User_a removes user_b as a channel owner
    channel_removeowner(user_a["token"], c_id_1, user_b["u_id"])

    # User_a removes user_b as a member
    channel_removemember(user_a["token"], c_id_1, user_b["u_id"])

    user_a_profile = (user_profile(user_a["token"], user_a["u_id"]))["user"]

    # Check that user_b was successfully removed from channel_1
    assert channel_details(user_a["token"], c_id_1) == {
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

    clear()


def test_channel_removemember_success_remove_owner(user_a, user_b):
    """
    Test 3 - Tests that an admin can successfully remove an owner
    from the channel
    """
    # User_b makes a channel
    channel_1 = channels_create(user_b["token"], "billionaire records", True)
    c_id_1 = channel_1["channel_id"]

    # User_a (admin of Flockr) joins the channel
    channel_join(user_a["token"], c_id_1)

    # User_a removes user_b as a member
    channel_removemember(user_a["token"], c_id_1, user_b["u_id"])

    user_a_profile = (user_profile(user_a["token"], user_a["u_id"]))["user"]

    # Check that user_b was successfully removed from channel_1
    assert channel_details(user_a["token"], c_id_1) == {
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

    clear()


def test_channel_removemember_invalid_uid(user_a):
    """
    Test 4 - InputError - Invalid u_id
    """
    # User_a makes a channel
    channel_1 = channels_create(user_a["token"], "billionaire records", True)
    c_id_1 = channel_1["channel_id"]

    # Error should be raised since u_id is invalid
    invalid_uid = 696969
    with pytest.raises(InputError, match=r"Invalid User ID"):
        channel_removemember(user_a["token"], c_id_1, invalid_uid)

    clear()


def test_channel_removemember_invalid_cid(user_a, user_b):
    """
    Test 5 - InputError - Invalid channel ID
    """
    # Error should be raised since channel ID is invalid
    invalid_cid = 696969
    with pytest.raises(InputError):
        channel_removemember(user_a["token"], invalid_cid, user_b["u_id"])

    clear()


def test_channel_removemember_self(user_a):
    """
    Test 6 - InputError - User attempts to remove themselves from channel
    """
    # User_a makes a channel
    channel_1 = channels_create(user_a["token"], "billionaire records", True)
    c_id_1 = channel_1["channel_id"]

    # Error should be raised since user cannot remove themselves from channel
    with pytest.raises(InputError, match=r"Removing yourself from the channel is not allowed"):
        channel_removemember(user_a["token"], c_id_1, user_a["u_id"])

    clear()


def test_channel_removemember_unauth(user_a, user_b):
    """
    Test 7 - AccessError - User attempting remove another
    user is not an admin of the flockr, or an owner of the
    channel
    """
    # User_b makes a channel
    channel_1 = channels_create(user_b["token"], "billionaire records", True)
    c_id_1 = channel_1["channel_id"]

    # User_a joins the channel
    channel_join(user_a["token"], c_id_1)

    # User_a removes user_b as an owner
    channel_removeowner(user_a["token"], c_id_1, user_b["u_id"])

    # Error should be raised since user_b is not authorised to remove members
    with pytest.raises(AccessError, match=r"User is not an owner"):
        channel_removemember(user_b["token"], c_id_1, user_a["u_id"])

    clear()


def test_channel_removemember_invalid_token(user_a):
    """
    Test 8 - AccessError - Invalid token
    """
    # User_a makes a channel
    channel_1 = channels_create(user_a["token"], "billionaire records", True)
    c_id_1 = channel_1["channel_id"]

    # Error should be raised since token passed in is invalid
    invalid_token = ""
    with pytest.raises(AccessError, match=r"Invalid Token"):
        channel_removeowner(invalid_token, c_id_1, user_a["u_id"])

    clear()
