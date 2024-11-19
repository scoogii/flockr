"""
channel_addowner

Takes in (token, channel_id, u_id)
Returns {}

Description: Make user with user id u_id an owner of this channel

Exceptions:
- InputError when any of:
    - Channel ID is not a valid channel
    - When user with user id u_id is already an owner of the channel
- AccessError when the authorised user is not an owner of the flockr, or an
owner of this channel
"""


import pytest
from auth import auth_register
from channel import channel_join, channel_details, channel_addowner
from channels import channels_create
from error import InputError, AccessError
from other import clear
from user import user_profile
from conftest import user_a, user_b, user_c


def test_channel_addowner_success(user_a, user_b):
    """
    Test 1 - Success when adding user as another owner
    """
    # User_a makes a channel
    channel_1 = channels_create(user_a["token"], "billionaire records", True)
    c_id_1 = channel_1["channel_id"]

    # User_b joins the channel
    channel_join(user_b["token"], c_id_1)

    # User_a makes second user the secondary owner
    channel_addowner(user_a["token"], c_id_1, user_b["u_id"])

    token = user_a["token"]

    # Retrieve user_profile
    user_a = (user_profile(user_a["token"], user_a["u_id"]))["user"]
    user_b = (user_profile(user_b["token"], user_b["u_id"]))["user"]

    # Checks
    assert channel_details(token, c_id_1) == {
        "name": "billionaire records",
        "owner_members": [
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


def test_admin_permission_success(user_a, user_b, user_c):
    """
    Test 2 - Success when admin adds another member as owner
    """
    # User_b creates the channel
    channel_1 = channels_create(user_b["token"], "billionaire records", True)
    c_id_1 = channel_1["channel_id"]

    # User_a is an admin by default and joins
    channel_join(user_a["token"], c_id_1)

    # User_c joins the channel
    channel_join(user_c["token"], c_id_1)

    # User_a makes user_c an owner of the channel
    channel_addowner(user_a["token"], c_id_1, user_c["u_id"])

    token = user_b["token"]

    # Retrieve user_profile
    user_a = (user_profile(user_a["token"], user_a["u_id"]))["user"]
    user_b = (user_profile(user_b["token"], user_b["u_id"]))["user"]
    user_c = (user_profile(user_c["token"], user_c["u_id"]))["user"]

    # Checks
    assert channel_details(token, c_id_1) == {
        "name": "billionaire records",
        "owner_members": [
            {
                "u_id": user_b["u_id"],
                "name_first": user_b["name_first"],
                "name_last": user_b["name_last"],
                "profile_img_url": user_b["profile_img_url"],
            },
            {
                "u_id": user_c["u_id"],
                "name_first": user_c["name_first"],
                "name_last": user_c["name_last"],
                "profile_img_url": user_c["profile_img_url"],
            },
        ],
        "all_members": [
            {
                "u_id": user_b["u_id"],
                "name_first": user_b["name_first"],
                "name_last": user_b["name_last"],
                "profile_img_url": user_b["profile_img_url"],
            },
            {
                "u_id": user_a["u_id"],
                "name_first": user_a["name_first"],
                "name_last": user_a["name_last"],
                "profile_img_url": user_a["profile_img_url"],
            },
            {
                "u_id": user_c["u_id"],
                "name_first": user_c["name_first"],
                "name_last": user_c["name_last"],
                "profile_img_url": user_c["profile_img_url"],
            },
        ],
    }

    clear()


def test_channel_addowner_invalid(user_a, user_b):
    """
    Test 4 - InputError - for invalid channel ID
    """
    # User_a makes a channel
    channel_1 = channels_create(user_a["token"], "billionaire records", True)
    c_id_1 = channel_1["channel_id"]

    # User_b joins the channel
    channel_join(user_b["token"], c_id_1)

    invalid_c_id = 4566343

    # User_b cannot be made owner because id is invalid
    with pytest.raises(InputError):
        channel_addowner(user_a["token"], invalid_c_id, user_b["u_id"])

    clear()


def test_channel_addowner_already(user_a, user_b):
    """
    Test 5 - InputError - for when user is already owner
    """
    # User_a makes a channel
    channel_1 = channels_create(user_a["token"], "billionaire records", True)
    c_id_1 = channel_1["channel_id"]

    # User_b joins the channel
    channel_join(user_b["token"], c_id_1)

    # User_a makes second user the secondary owner
    channel_addowner(user_a["token"], c_id_1, user_b["u_id"])

    # User_b tries to be made owner again
    with pytest.raises(InputError, match=r"User is already an owner"):
        channel_addowner(user_a["token"], c_id_1, user_b["u_id"])

    clear()


def test_channel_addowner_unauth(user_a, user_b, user_c):
    """
    Test 6 - AccessError - for adding another user but that user isn't the owner
    """
    # User_a makes a channel
    channel_1 = channels_create(user_a["token"], "billionaire records", True)
    c_id_1 = channel_1["channel_id"]

    # User_b joins the channel
    channel_join(user_b["token"], c_id_1)

    # User_c user joins the channel
    channel_join(user_c["token"], c_id_1)

    # User_c cannot be made owner because User_b isn't owner
    with pytest.raises(AccessError, match=r"User is not an owner"):
        channel_addowner(user_b["token"], c_id_1, user_c["u_id"])

    clear()


def test_channel_addowner_invalid_token(user_a, user_b):
    """
    Test 7 -  AccessError - Invalid token passed in
    """
    # User_a creates channel
    channel_1 = channels_create(user_a["token"], "billionaire records", True)
    c_id_1 = channel_1["channel_id"]
    invalid_token = ""

    # User_b joins the channel
    channel_join(user_b["token"], c_id_1)

    # AccessError should be raised since token passed is invalid
    with pytest.raises(AccessError, match=r"Invalid Token"):
        channel_addowner(invalid_token, c_id_1, user_b["u_id"])

    clear()
