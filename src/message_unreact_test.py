"""
message_unreact

Takes in parameters 'token', 'message_id', 'react_id'
Returns {}

Description: Given a message, remove a react to that particular message

Exceptions:
- InputError:
    - when message_id is invalid
    - react_id is invalid (currently, the only valid react_id is 1)
    - message does not contain an active react with the same react_id
"""

import pytest
from auth import auth_register
from channel import channel_join, channel_messages
from channels import channels_create
from data import DATA
from error import InputError
from message import message_send, message_react, message_unreact
from other import clear
from conftest import user_a, user_b, user_c


def get_time_created(m_id):
    """
    Retrieves the time_created for a message given a message_id
    """
    for message in DATA["message_log"]["messages"]:
        if m_id == message["message_id"]:
            return message["time_created"]


def test_message_unreact_success_own_message(user_a):
    """
    Test 1 - user successfully unreacts to their own message
    """
    # User_a creates a channel and becomes the owner
    channel_1 = channels_create(user_a["token"], "billionaire records", True)
    c_id_1 = channel_1["channel_id"]

    # Send a message to the channel
    msg_1 = message_send(user_a["token"], c_id_1, "Throw it out the window")
    m_id_1 = msg_1["message_id"]

    # React to the message that is sent
    react_id_1 = 1
    message_react(user_a["token"], m_id_1, react_id_1)

    # Unreact to the message
    message_unreact(user_a["token"], m_id_1, react_id_1)

    # Check that the message has been unreacted to
    assert channel_messages(user_a["token"], c_id_1, 0) == {
        "messages": [
            {
                "message_id": m_id_1,
                "u_id": user_a["u_id"],
                "message": "Throw it out the window",
                "time_created": get_time_created(m_id_1),
                "reacts": [
                    {
                        "react_id": 1,
                        "u_ids": [],
                        "is_this_user_reacted": False,
                    },
                ],
                "is_pinned": False,
            },
        ],
        "start": 0,
        "end": -1,
    }

    clear()


def test_message_unreact_success_other_message(user_a, user_b):
    """
    Test 2 - user successfully unreacts to a message that is not their own
    """
    # User_a creates a channel and becomes the owner
    channel_1 = channels_create(user_a["token"], "billionaire records", True)
    c_id_1 = channel_1["channel_id"]

    # User_b joins the created channel
    channel_join(user_b["token"], c_id_1)

    # User_b sends a message to the channel
    msg_1 = message_send(user_b["token"], c_id_1, "Throw it out the window")
    m_id_1 = msg_1["message_id"]

    # User_a reacts to user_b's message
    react_id_1 = 1
    message_react(user_a["token"], m_id_1, react_id_1)

    # User_a unreacts to the message
    message_unreact(user_a["token"], m_id_1, react_id_1)

    # Check that the message has been unreacted to
    assert channel_messages(user_a["token"], c_id_1, 0) == {
        "messages": [
            {
                "message_id": m_id_1,
                "u_id": user_b["u_id"],
                "message": "Throw it out the window",
                "time_created": get_time_created(m_id_1),
                "reacts": [
                    {
                        "react_id": 1,
                        "u_ids": [],
                        "is_this_user_reacted": False,
                    },
                ],
                "is_pinned": False,
            },
        ],
        "start": 0,
        "end": -1,
    }

    clear()


def test_message_unreact_success_multiple_1(user_a, user_b, user_c):
    """
    Test 3 - user successfully unreacts to a message, other user's reacts
    should still appear
    User who unreacted calls channel_messages, is_this_user_reacted should be False
    """
    # User_a creates a channel and becomes the owner
    channel_1 = channels_create(user_a["token"], "billionaire records", True)
    c_id_1 = channel_1["channel_id"]

    # User_b and user_c join the created channel
    channel_join(user_b["token"], c_id_1)
    channel_join(user_c["token"], c_id_1)

    # User_b sends a message to the channel
    msg_1 = message_send(user_b["token"], c_id_1, "Throw it out the window")
    m_id_1 = msg_1["message_id"]

    # User_a and user_c reacts to user_b's message
    react_id_1 = 1
    message_react(user_a["token"], m_id_1, react_id_1)
    message_react(user_c["token"], m_id_1, react_id_1)

    # User_a unreacts to the message
    message_unreact(user_a["token"], m_id_1, react_id_1)

    # User_a checks that the message has been unreacted
    assert channel_messages(user_a["token"], c_id_1, 0) == {
        "messages": [
            {
                "message_id": m_id_1,
                "u_id": user_b["u_id"],
                "message": "Throw it out the window",
                "time_created": get_time_created(m_id_1),
                "reacts": [
                    {
                        "react_id": 1,
                        "u_ids": [user_c["u_id"]],
                        "is_this_user_reacted": False,
                    },
                ],
                "is_pinned": False,
            },
        ],
        "start": 0,
        "end": -1,
    }

    clear()


def test_message_unreact_success_multiple_2(user_a, user_b, user_c):
    """
    Test 4 - user successfully unreacts to a message, other user's reacts
    should still appear
    User who did not unreact calls channel_messages, is_this_user_reacted should be True
    """
    # User_a creates a channel and becomes the owner
    channel_1 = channels_create(user_a["token"], "billionaire records", True)
    c_id_1 = channel_1["channel_id"]

    # User_b and user_c join the created channel
    channel_join(user_b["token"], c_id_1)
    channel_join(user_c["token"], c_id_1)

    # User_b sends a message to the channel
    msg_1 = message_send(user_b["token"], c_id_1, "Throw it out the window")
    m_id_1 = msg_1["message_id"]

    # User_a and user_c reacts to user_b's message
    react_id_1 = 1
    message_react(user_a["token"], m_id_1, react_id_1)
    message_react(user_c["token"], m_id_1, react_id_1)

    # User_a unreacts to the message
    message_unreact(user_a["token"], m_id_1, react_id_1)

    # User_c checks that the message has been unreacted
    assert channel_messages(user_c["token"], c_id_1, 0) == {
        "messages": [
            {
                "message_id": m_id_1,
                "u_id": user_b["u_id"],
                "message": "Throw it out the window",
                "time_created": get_time_created(m_id_1),
                "reacts": [
                    {
                        "react_id": 1,
                        "u_ids": [user_c["u_id"]],
                        "is_this_user_reacted": True,
                    },
                ],
                "is_pinned": False,
            },
        ],
        "start": 0,
        "end": -1,
    }

    clear()


def test_message_unreact_success_multiple_messages(user_a, user_b):
    """
    Test 5 - user successfully unreacts to multiple messages
    """
    # User_a creates a channel and becomes the owner
    channel_1 = channels_create(user_a["token"], "billionaire records", True)
    c_id_1 = channel_1["channel_id"]

    # User_b joins the created channel
    channel_join(user_b["token"], c_id_1)

    # User_b sends 2 messages to the channel
    msg_1 = message_send(user_b["token"], c_id_1, "Throw it out the window")
    m_id_1 = msg_1["message_id"]
    msg_2 = message_send(user_b["token"], c_id_1, "I like trains")
    m_id_2 = msg_2["message_id"]

    # User_a reacts to both of user_b's message
    react_id_1 = 1
    message_react(user_a["token"], m_id_1, react_id_1)
    message_react(user_a["token"], m_id_2, react_id_1)

    # User_a unreacts to both of the messages
    message_unreact(user_a["token"], m_id_1, react_id_1)
    message_unreact(user_a["token"], m_id_2, react_id_1)

    # User_a checks that both the message have been unreacted
    assert channel_messages(user_a["token"], c_id_1, 0) == {
        "messages": [
            {
                "message_id": m_id_2,
                "u_id": user_b["u_id"],
                "message": "I like trains",
                "time_created": get_time_created(m_id_2),
                "reacts": [
                    {
                        "react_id": 1,
                        "u_ids": [],
                        "is_this_user_reacted": False,
                    },
                ],
                "is_pinned": False,
            },
            {
                "message_id": m_id_1,
                "u_id": user_b["u_id"],
                "message": "Throw it out the window",
                "time_created": get_time_created(m_id_1),
                "reacts": [
                    {
                        "react_id": 1,
                        "u_ids": [],
                        "is_this_user_reacted": False,
                    },
                ],
                "is_pinned": False,
            },
        ],
        "start": 0,
        "end": -1,
    }

    clear()


def test_message_unreact_invalid_message_id(user_a):
    """
    Test 6 - InputError - User tries to unreact to a message with an
    invalid message_id
    """
    invalid_m_id = 123456

    with pytest.raises(InputError):
        react_id_1 = 1
        message_unreact(user_a["token"], invalid_m_id, react_id_1)

    clear()


def test_message_unreact_invalid_react_id(user_a):
    """
    Test 7 - InputError - User tries to unreact to a message with an
    invalid react_id
    """
    # User_a creates a channel and becomes the owner
    channel_1 = channels_create(user_a["token"], "billionaire records", True)
    c_id_1 = channel_1["channel_id"]

    # Send a message to the channel
    msg_1 = message_send(user_a["token"], c_id_1, "Throw it out the window")
    m_id_1 = msg_1["message_id"]

    react_id_1 = 1
    message_react(user_a["token"], m_id_1, react_id_1)

    with pytest.raises(InputError):
        invalid_react_id = 123456
        message_unreact(user_a["token"], m_id_1, invalid_react_id)

    clear()


def test_message_unreact_invalid_inexistent_react(user_a):
    """
    Test 8 - InputError - User tries to unreact to a message that does not
    have an active react
    """
    # User_a creates a channel and becomes the owner
    channel_1 = channels_create(user_a["token"], "billionaire records", True)
    c_id_1 = channel_1["channel_id"]

    # Send a message to the channel
    msg_1 = message_send(user_a["token"], c_id_1, "Throw it out the window")
    m_id_1 = msg_1["message_id"]

    with pytest.raises(InputError):
        react_id_1 = 1
        message_unreact(user_a["token"], m_id_1, react_id_1)

    clear()
