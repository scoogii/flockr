"""
channel_removeowner

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
from channel import channel_join, channel_details, channel_addowner, channel_removeowner
from channels import channels_create
from error import InputError, AccessError
from find import find_user_from_token
from other import clear
from user import user_profile
from conftest import user_a, user_b, user_c


def test_channel_removeowner_success(user_a, user_b):
    """
    Test 1 - testing that user is successfully removed as owner
    """
    # First user makes a channel
    channel_1 = channels_create(user_a["token"], "billionaire records", True)
    c_id_1 = channel_1["channel_id"]

    # Second user joins the channel
    channel_join(user_b["token"], c_id_1)

    # First user makes second user the secondary owner
    channel_addowner(user_a["token"], c_id_1, user_b["u_id"])

    # First user removes second user as secondary owner
    channel_removeowner(user_a["token"], c_id_1, user_b["u_id"])

    token = user_a["token"]

    user_a = (user_profile(user_a["token"], user_a["u_id"]))["user"]
    user_b = (user_profile(user_b["token"], user_b["u_id"]))["user"]

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


def test_channel_removeowner_admin_success(user_a, user_b):
    """
    Test 2 - testing that an admin can remove a channel owner
    """
    # Second user makes a channel
    channel_1 = channels_create(user_b["token"], "billionaire records", True)
    c_id_1 = channel_1["channel_id"]

    # User_a who is an admin joins the channel
    channel_join(user_a["token"], c_id_1)

    # User_a removes user_b as an owner of the channel
    channel_removeowner(user_a["token"], c_id_1, user_b["u_id"])

    token = user_a["token"]

    user_a = (user_profile(user_a["token"], user_a["u_id"]))["user"]
    user_b = (user_profile(user_b["token"], user_b["u_id"]))["user"]

    assert channel_details(token, c_id_1) == {
        "name": "billionaire records",
        "owner_members": [],
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
        ],
    }

    clear()


def test_channel_removeowner_invalid(user_a, user_b):
    """
    Test 3 - InputError - for invalid channel ID
    """
    # First user makes a channel
    channel_1 = channels_create(user_a["token"], "billionaire records", True)
    c_id_1 = channel_1["channel_id"]

    # Second user joins the channel
    channel_join(user_b["token"], c_id_1)

    # First user makes second user the secondary owner
    channel_addowner(user_a["token"], c_id_1, user_b["u_id"])

    invalid_c_id = 4566343

    # User 2 cannot be removed as owner because id is invalid
    with pytest.raises(InputError):
        channel_removeowner(user_a["token"], invalid_c_id, user_b["u_id"])

    clear()


def test_channel_removeowner_unauth(user_a, user_b, user_c):
    """
    Test 4 - AccessError - for removing another user but that user isn't the owner
    """
    # First user makes a channel
    channel_1 = channels_create(user_a["token"], "billionaire records", True)
    c_id_1 = channel_1["channel_id"]

    # Second user joins the channel
    channel_join(user_b["token"], c_id_1)

    # Third user joins the channel
    channel_join(user_c["token"], c_id_1)

    # User 3 cannot be removed owner because user 2 isn't owner
    with pytest.raises(AccessError, match=r"User is not an owner"):
        channel_removeowner(user_b["token"], c_id_1, user_c["u_id"])

    clear()


def test_channel_uid_not_owner(user_a, user_b):
    """
    Test 5 - InputError - for removing another user but that user isn't the owner
    """
    # First user makes a channel
    channel_1 = channels_create(user_a["token"], "billionaire records", True)
    c_id_1 = channel_1["channel_id"]

    # Second user joins the channel
    channel_join(user_b["token"], c_id_1)

    # User 3 cannot be removed owner because user 2 isn't owner
    with pytest.raises(
        InputError, match=r"User being removed as owner is not an owner"
    ):
        channel_removeowner(user_a["token"], c_id_1, user_b["u_id"])

    clear()


def test_channel_removeowner_invalid_token(user_a, user_b):
    """
    Test 6 - AccessError - invalid token given
    """
    # First user makes a channel
    channel_2 = channels_create(user_a["token"], "no token", True)
    c_id_2 = channel_2["channel_id"]

    channel_addowner(user_a["token"], c_id_2, user_b["u_id"])

    # Cannot remove owner since invalid token was given
    with pytest.raises(AccessError, match=r"Invalid Token"):
        channel_removeowner("invalid_token", c_id_2, user_b["u_id"])

    clear()
