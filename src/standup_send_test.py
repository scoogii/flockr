"""
standup_send

Takes in (token, channel_id, length)
Returns {}

Description: Sending a message to get buffered in the standup queue,
assuming a standup is currently active

Exceptions:
- InputError when any of:
    - Channel ID is not a valid channel
    - Message is more than 1000 characters
    - An active standup is currently running in this channel

- AccessError when any of:
    - The authorised user is not a member of the channel that the message is within

"""


import pytest
from time import sleep
from channel import channel_messages
from channels import channels_create
from data import DATA
from message import message_send
from error import InputError, AccessError
from standup import standup_start, standup_send
from user import user_profile
from other import clear
from conftest import user_a, user_b


def get_time_created(m_id):
    """
    Retrieves the time_created for a message given a message_id
    """
    for message in DATA["message_log"]["messages"]:
        if m_id == message["message_id"]:
            return message["time_created"]


def test_standup_send_test_1(user_a):
    """
    Test 1 - Standup send success
    """
    # User_a makes a channel
    channel_1 = channels_create(user_a["token"], "billionaire records", True)
    c_id_1 = channel_1["channel_id"]

    # User_a sends a message
    message_send(user_a["token"], c_id_1, "/standup 5")

    # Standup start
    standup_start(user_a["token"], c_id_1, 5)

    # Send a message within standup
    standup_send(user_a["token"], c_id_1, "Throw it out the window")

    # Wait 6 seconds
    sleep(6)

    # Get user's handle
    user_a_profile = user_profile(user_a["token"], user_a["u_id"])
    user_a_handle = user_a_profile["user"]["handle_str"]

    # Check that the standup message was sent successfully
    assert channel_messages(user_a["token"], c_id_1, 0) == {
        "messages": [
            {
                "message_id": 2,
                "u_id": 1,
                "message": f"{user_a_handle}: Throw it out the window\n",
                "time_created": get_time_created(2),
                "reacts": [
                    {
                        "react_id": 1,
                        "u_ids": [],
                        "is_this_user_reacted": False,
                    }
                ],
                "is_pinned": False
            },
            {
                "message_id": 1,
                "u_id": 1,
                "message": "/standup 5",
                "time_created": get_time_created(1),
                "reacts": [
                    {
                        "react_id": 1,
                        "u_ids": [],
                        "is_this_user_reacted": False,
                    }
                ],
                "is_pinned": False,
            }
        ],
        "start": 0,
        "end": -1,
    }

    clear()


def test_standup_send_simultaneous(user_a):
    """
    Test 2 - Simultaneous standup send success
    """
    # User_a makes a channel
    channel_1 = channels_create(user_a["token"], "billionaire records", True)
    c_id_1 = channel_1["channel_id"]

    # User_a makes another channel
    channel_2 = channels_create(user_a["token"], "the cage", True)
    c_id_2 = channel_2["channel_id"]

    # User_a starts a standup in channel 1
    standup_start(user_a["token"], c_id_1, 5)

    # User_a starts a standup in channel 2
    standup_start(user_a["token"], c_id_2, 5)

    # User_a sends a message during standup in channel 1
    standup_send(user_a["token"], c_id_2, "Throw it out the window")

    # Wait 6 seconds
    sleep(6)

    # Get user's handle
    user_a_profile = user_profile(user_a["token"], user_a["u_id"])
    user_a_handle = user_a_profile["user"]["handle_str"]

    # Check that the standup message was sent successfully
    assert channel_messages(user_a["token"], c_id_2, 0) == {
        "messages": [
            {
                "message_id": 1,
                "u_id": 1,
                "message": f"{user_a_handle}: Throw it out the window\n",
                "time_created": get_time_created(1),
                "reacts": [
                    {
                        "react_id": 1,
                        "u_ids": [],
                        "is_this_user_reacted": False,
                    }
                ],
                "is_pinned": False
            },
        ],
        "start": 0,
        "end": -1,
    }

    clear()


def test_standup_send_test_invalid_c_id(user_a):
    """
    Test 3 - InputError - invalid channel ID
    """
    # User_a makes a channel
    channel_1 = channels_create(user_a["token"], "billionaire records", True)
    c_id_1 = channel_1["channel_id"]

    # User_a sends a message
    message_send(user_a["token"], c_id_1, "/standup 200")

    # Standup start
    standup_start(user_a["token"], c_id_1, 200)

    invalid_c_id = 12345

    # Error should be raised since channel_id is invalid
    with pytest.raises(InputError):
        standup_send(user_a["token"], invalid_c_id, "Throw it out the window")

    clear()


def test_standup_send_test_too_long(user_a):
    """
    Test 4 - InputError - Message over 1000 characters
    """

    # User_a makes a channel
    channel_1 = channels_create(user_a["token"], "billionaire records", True)
    c_id_1 = channel_1["channel_id"]

    # User_a sends a message
    message_send(user_a["token"], c_id_1, "Hello")

    # Standup start
    standup_start(user_a["token"], c_id_1, 200)

    # Error should be raised since message is too long
    with pytest.raises(InputError, match=r"Messages should be between 0 and 1000 characters long"):
        standup_send(user_a["token"], c_id_1, "Hello"*1000)

    clear()


def test_standup_send_test_inactive(user_a):
    """
    Test 5 - InputError - No active standup running
    """
    # User_a makes a channel
    channel_1 = channels_create(user_a["token"], "billionaire records", True)
    c_id_1 = channel_1["channel_id"]

    # User_a sends a message
    message_send(user_a["token"], c_id_1, "Hello")

    # Send a message within standup
    with pytest.raises(InputError, match=r"Standup is not running"):
        standup_send(user_a["token"], c_id_1, "Throw it out the window")

    clear()


def test_standup_send_test_not_part(user_a, user_b):
    """
    Test 6 - AccessError - No active standup running
    """
    # User_a makes a channel
    channel_1 = channels_create(user_a["token"], "billionaire records", True)
    c_id_1 = channel_1["channel_id"]

    # User_a sends a message
    message_send(user_a["token"], c_id_1, "Hello")

    # Standup start
    standup_start(user_a["token"], c_id_1, 200)

    # Error should be raised since there is no active standup
    with pytest.raises(AccessError, match=r"You must be a member of the channel to view its details"):
        standup_send(user_b["token"], c_id_1, "Throw it out the window")

    clear()
