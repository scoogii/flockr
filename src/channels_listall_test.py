"""
channels_listall

Takes in one parameter `token`
Returns a dictionary {channels}

Description: Provides a list of all channels (and their associated details)

Exceptions:
 - AccessError: should occur when an Invalid Token is passed in
"""


import pytest
from auth import auth_register
from channels import channels_create, channels_listall
from error import AccessError
from other import clear
from conftest import user_a, user_b


def test_channels_listall_none(user_a):
    """
    Test 1 - Listing all channels when no channels exist
    """
    # channels_listall should return a dictionary with empty channels
    assert channels_listall(user_a["token"]) == {"channels": []}

    clear()


def test_channels_listall_same_user(user_a):
    """
    Test 2 - Listing all channels when all have been created by same user
    Account for public and private channels
    """
    # User_a makes a public channel
    channel_1 = channels_create(user_a["token"], "billionaire records", True)
    c_id_1 = channel_1["channel_id"]

    # Create second channel by the same user
    channel_2 = channels_create(user_a["token"], "the cage", False)
    c_id_2 = channel_2["channel_id"]

    # channels_listall should return both public and private created channels
    assert channels_listall(user_a["token"]) == {
        "channels": [
            {
                "channel_id": c_id_1,
                "name": "billionaire records",
            },
            {
                "channel_id": c_id_2,
                "name": "the cage",
            },
        ]
    }

    clear()


def test_channels_listall_multiple_users(user_a, user_b):
    """
    Test 3 - Listing all channels created by multiple users
    """
    # User_a creates a public channel
    channel_1 = channels_create(user_a["token"], "billionaire records", True)
    c_id_1 = channel_1["channel_id"]

    # User_b creates a private channel
    channel_2 = channels_create(user_b["token"], "the cage", False)
    c_id_2 = channel_2["channel_id"]

    # channels_listall should return the channels created by both users
    assert channels_listall(user_a["token"]) == {
        "channels": [
            {
                "channel_id": c_id_1,
                "name": "billionaire records",
            },
            {
                "channel_id": c_id_2,
                "name": "the cage",
            },
        ]
    }

    clear()


def test_channels_listall_invalid_token():
    """
    Test 4 - AccessError - Invalid Token passed in
    (refer to assumptions)
    """
    invalid_token = ""

    # AccessError should be raised since token passed is invalid
    with pytest.raises(AccessError, match=r"Invalid Token"):
        channels_listall(invalid_token)

    clear()
