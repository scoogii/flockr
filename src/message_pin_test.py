"""
message_pin

Takes in parameters `token`, `message_id`

Description: Given a message within a channel, mark it as
"pinned" to be given special display treatment by the
frontend

Exceptions:
  - InputError when any of:
    - message_id is not a valid channel message
    - Message with ID message_id is already pinned
 - AccessError when any of:
    - The authorised user is not a member of the channel
    that the message is within
    - The authorised user is not an owner
"""


import pytest
from auth import auth_register
from channel import channel_join, channel_messages
from channels import channels_create
from data import DATA
from error import AccessError, InputError
from message import message_send, message_pin
from other import clear
from conftest import user_a, user_b


def get_time_created(m_id):
    """
    Retrieves the time_created for a message given a message_id
    """
    for message in DATA["message_log"]["messages"]:
        if m_id == message["message_id"]:
            return message["time_created"]


def test_message_pin_success(user_a, user_b):
    """
    Test 1 - Message is successfully pinned by the owner of the channel
    """
    # User_a makes a channel
    channel_1 = channels_create(user_a["token"], "billionaire records", True)
    c_id_1 = channel_1["channel_id"]

    # User_b joins and sends a message
    channel_join(user_b["token"], c_id_1)
    message_1 = message_send(user_b["token"], c_id_1, "Throw it out the window")
    m_id_1 = message_1["message_id"]

    # User_a pins the message
    message_pin(user_a["token"], m_id_1)

    # Check that the message has been pinned successfully
    assert channel_messages(user_a["token"], c_id_1, 0) == {
        "messages": [
            {
                "message_id": 1,
                "u_id": user_b["u_id"],
                "message": "Throw it out the window",
                "time_created": get_time_created(m_id_1),
                "reacts": [
                    {
                        "react_id": 1,
                        "u_ids": [],
                        "is_this_user_reacted": False,
                    }
                ],
                "is_pinned": True,
            }
        ],
        "start": 0,
        "end": -1,
    }

    clear()


def test_message_pin_multiple(user_a):
    """
    Test 2 - Testing that pinning multiple messages is successful
    """
    # User_a makes a channel
    channel_1 = channels_create(user_a["token"], "billionaire records", True)
    c_id_1 = channel_1["channel_id"]

    # User_a sends a message
    message_1 = message_send(user_a["token"], c_id_1, "Throw it out the window")
    m_id_1 = message_1["message_id"]

    # User_a sends another message
    message_2 = message_send(user_a["token"], c_id_1, "I like trains")
    m_id_2 = message_2["message_id"]

    # User_a pins both messages
    message_pin(user_a["token"], m_id_1)
    message_pin(user_a["token"], m_id_2)

    # Check that the messages have been pinned successfully
    assert channel_messages(user_a["token"], c_id_1, 0) == {
        "messages": [
            {
                "message_id": 2,
                "u_id": user_a["u_id"],
                "message": "I like trains",
                "time_created": get_time_created(m_id_1),
                "reacts": [
                    {
                        "react_id": 1,
                        "u_ids": [],
                        "is_this_user_reacted": False,
                    }
                ],
                "is_pinned": True,
            },
            {
                "message_id": 1,
                "u_id": user_a["u_id"],
                "message": "Throw it out the window",
                "time_created": get_time_created(m_id_1),
                "reacts": [
                    {
                        "react_id": 1,
                        "u_ids": [],
                        "is_this_user_reacted": False,
                    }
                ],
                "is_pinned": True,
            },
        ],
        "start": 0,
        "end": -1,
    }

    clear()


def test_message_pin_invalid_mid(user_a):
    """
    Test 3 - InputError - Pinning a message with an invalid message_id
    """
    # User_a makes a channel
    channels_create(user_a["token"], "billionaire records", True)

    # Message is invalid since message_id does not belong to an existing message
    invalid_m_id = 4566343
    with pytest.raises(InputError):
        message_pin(user_a["token"], invalid_m_id)

    clear()


def test_message_pin_already_pinned(user_a, user_b):
    """
    Test 4 - InputError - Pinning a message that is already pinned
    """
    # User_a makes a channel
    channel_1 = channels_create(user_a["token"], "billionaire records", True)
    c_id_1 = channel_1["channel_id"]

    # User_b joins and sends a message
    channel_join(user_b["token"], c_id_1)
    message_1 = message_send(user_b["token"], c_id_1, "Throw it out the window")
    m_id_1 = message_1["message_id"]

    # User_a pins the message
    message_pin(user_a["token"], m_id_1)

    # Error should be raised since the message has already been pinned
    with pytest.raises(InputError, match=r"Message is already pinned"):
        message_pin(user_a["token"], m_id_1)

    clear()


def test_message_pin_not_in_channel(user_a, user_b):
    """
    Test 5 - AccessError - Pinning a message when user is not in the channel
    """
    # User_a makes a channel
    channel_1 = channels_create(user_a["token"], "billionaire records", True)
    c_id_1 = channel_1["channel_id"]

    # User_a sends a message
    message_1 = message_send(user_a["token"], c_id_1, "Throw it out the window")
    m_id_1 = message_1["message_id"]

    # Error should be raised since user_b isn't part of the channel the message was sent in
    with pytest.raises(AccessError, match=r"You must be a member of the channel to view its details"):
        message_pin(user_b["token"], m_id_1)

    clear()


def test_message_pin_unauth(user_a, user_b):
    """
    Test 6 - AccessError - Pinning a message when the user is not an owner/admin
    """
    # User_a makes a channel
    channel_1 = channels_create(user_a["token"], "billionaire records", True)
    c_id_1 = channel_1["channel_id"]

    # User_a sends a message
    message_1 = message_send(user_a["token"], c_id_1, "Throw it out the window")
    m_id_1 = message_1["message_id"]

    # User_b joins the channel
    channel_join(user_b["token"], c_id_1)

    # Error should be raised since user_b is not an owner of the channel or a flockr admin
    with pytest.raises(AccessError, match=r"You are not authorised to alter this channel"):
        message_pin(user_b["token"], m_id_1)

    clear()
