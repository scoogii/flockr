"""
channels_create

Takes in parameters `token`, `name`, `is_public`
Returns a dictionary {channel_id}

Description: Creates a new channel with that name that is either public
or private channel

Exceptions:
 - InputError - should occur when name
   is less than 3 or more than 20 characters long
 - AccessError - should occur when an Invalid Token is passed in
"""


import pytest
from auth import auth_register
from channels import channels_create, channels_listall
from error import InputError, AccessError
from other import clear
from conftest import user_a, user_b

def test_channels_create_public_success(user_a):
    """
    Test 1 - Test that public channels are successfully created
    """
    # User creates a public channel
    channel_1 = channels_create(user_a["token"], "billionaire records", True)
    c_id_1 = channel_1["channel_id"]

    # If channel was successfully added, it should be shown from listall
    assert channels_listall(user_a["token"]) == {
        "channels": [
            {
                "channel_id": c_id_1,
                "name": "billionaire records",
            },
        ]
    }

    clear()


def test_channels_create_private_success(user_a):
    """
    Test 2 - Test that private channels are successfully created
    """
    # User creates a private channel
    channel_2 = channels_create(user_a["token"], "the cage", False)
    c_id_2 = channel_2["channel_id"]

    # If channel was successfully added, it should be shown from listall
    assert channels_listall(user_a["token"]) == {
        "channels": [
            {
                "channel_id": c_id_2,
                "name": "the cage",
            },
        ]
    }

    clear()


def test_channels_create_too_long_just_above(user_a):
    """
    Test 3 - InputError - name too long, just above maximum
    """
    # InputError should occur when name is more than 20 characters long
    with pytest.raises(InputError, match=r"Channel name too long"):
        channels_create(user_a["token"], 21 * "A", True)

    clear()


def test_channels_create_too_long_excessive(user_a):
    """
    Test 4 - InputError - name too long, excessive number of characters
    """
    # InputError should occur when name is more than 20 characters long
    with pytest.raises(InputError, match=r"Channel name too long"):
        channels_create(user_a["token"], 50 * "A", True)

    clear()


def test_channels_create_invalid_token():
    """
    Test 5 - AccessError - Invalid token passed in
    (refer to assumptions)
    """
    invalid_token = ""

    # AccessErorr should be raised since token passed is invalid
    with pytest.raises(AccessError, match=r"Invalid Token"):
        channels_create(invalid_token, "billionaire records", True)

    clear()
