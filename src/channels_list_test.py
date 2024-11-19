"""
channels_list

Takes in the parameter `token`
Returns a dictionary {channels}

Description: Provides a list of all channels (and their associated detaisl)
that the authorised user is part of

Exceptions:
 - AccessError - should occur when an Invalid Token is passed in
"""


import pytest
from auth import auth_register
from channel import channel_invite
from channels import channels_create, channels_list
from error import AccessError
from other import clear
from conftest import user_a, user_b


def test_channels_list_none(user_a):
    """
    Test 1 - Listing channels when the user is not in any channel
    """
    # channel_list should return a dictionary with empty channels
    assert channels_list(user_a["token"]) == {"channels": []}

    clear()


def test_channels_list_pub(user_a):
    """
    Test 2 - Listing channels when the user is part of a public channel
    """
    # User_a makes a new public channel
    channel_1 = channels_create(user_a["token"], "billionaire records", True)
    c_id_1 = channel_1["channel_id"]

    # channels_list should return a dictionary with the public channel
    # that the user is part of
    assert channels_list(user_a["token"]) == {
        "channels": [
            {
                "channel_id": c_id_1,
                "name": "billionaire records",
            },
        ]
    }

    clear()


def test_channels_list_priv(user_a, user_b):
    """
    Test 3 - Listing channels when the user is part of a private channel
    """
    # User_a creates a new private channel
    channel_2 = channels_create(user_a["token"], "the cage", False)
    c_id_2 = channel_2["channel_id"]

    # User_a invites user_b to channel - second becomes authorised
    channel_invite(user_a["token"], c_id_2, user_b["u_id"])

    # channels_list should return a dictionary with the private channel
    assert channels_list(user_b["token"]) == {
        "channels": [
            {
                "channel_id": c_id_2,
                "name": "the cage",
            },
        ]
    }

    clear()


def test_channels_list_pub_priv(user_a, user_b):
    """
    Test 4 - Listing channels when the user is in
    both a public and private channel
    """
    # User_a user creates a new public channel
    channel_1 = channels_create(user_a["token"], "billionaire records", True)
    c_id_1 = channel_1["channel_id"]

    # User_a user creates a new public channel
    channel_2 = channels_create(user_a["token"], "the cage", False)
    c_id_2 = channel_2["channel_id"]

    # User_a user invites user_b to both created channels
    channel_invite(user_a["token"], c_id_1, user_b["u_id"])
    channel_invite(user_a["token"], c_id_2, user_b["u_id"])

    # channels_list should return a dictionary with both pub and priv channels
    assert channels_list(user_b["token"]) == {
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


def test_channels_list_some(user_a, user_b):
    """
    Test 5 - Lists channels that only user_a is considered
    an authorised user for
    """
    # User_a creates one channel
    channel_1 = channels_create(user_a["token"], "billionaire records", True)
    c_id_1 = channel_1["channel_id"]

    # User_b user creates another channel
    channels_create(user_b["token"], "the cage", False)

    # channels_list should return a dictionary the channel user_a is in
    assert channels_list(user_a["token"]) == {
        "channels": [
            {
                "channel_id": c_id_1,
                "name": "billionaire records",
            },
        ]
    }

    clear()


def test_channels_list_invalid_token(user_a):
    """
    Test 6 - AccessError - Invalid token passed in
    (refer to assumptions)
    """
    # User_a creates a channel
    channels_create(user_a["token"], "billionaire records", True)
    invalid_token = ""

    # AccessError should be raised since token passed is invalid
    with pytest.raises(AccessError, match=r"Invalid Token"):
        channels_list(invalid_token)

    clear()
