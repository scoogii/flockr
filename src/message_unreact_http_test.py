"""
message_unreact_http_test

Testing that message_unreact works with
http implementation
"""


import requests
from data import DATA
from echo_http_test import url
from conftest_http import user_a, user_b, user_c
from other import clear
from http_channel_functions import http_channel_join, http_channel_messages
from http_channels_functions import http_channels_create
from http_message_functions import http_message_send, http_message_react, http_message_unreact


def test_message_unreact_htto_success_own_message(url, user_a):
    """
    Test 1 - user successfully unreacts to their own message
    """
    # User_a makes a channel
    channel_1 = http_channels_create(url, user_a["token"], "billionaire records", True).json()
    c_id_1 = channel_1["channel_id"]

    # User_a sends a message to the channel
    msg_1 = http_message_send(url, user_a["token"], c_id_1, "Throw it out the window").json()
    m_id_1 = msg_1["message_id"]

    # User_a reacts to their own message
    http_message_react(url, user_a["token"], m_id_1, 1)

    # User_a unreacts to their own message
    http_message_unreact(url, user_a["token"], m_id_1, 1)

    # Check that the message has been unreacted to
    channel_msgs = http_channel_messages(url, user_a["token"], c_id_1, 0)

    result = channel_msgs.json()
    assert result == {
        "messages": [
            {
                "message_id": m_id_1,
                "u_id": user_a["u_id"],
                "message": "Throw it out the window",
                "time_created": result["messages"][0]["time_created"],
                "reacts": [
                    {
                        "react_id": 1,
                        "u_ids": [],
                        "is_this_user_reacted": False,
                    },
                ],
                "is_pinned": False,
            }
        ],
        "start": 0,
        "end": -1,
    }

    clear()


def test_message_unreact_http_success_other_message(url, user_a, user_b):
    """
    Test 2 - user successfully unreacts to a message that is not their own
    """
    # User_a makes a channel
    channel_1 = http_channels_create(url, user_a["token"], "billionaire records", True).json()
    c_id_1 = channel_1["channel_id"]

    # User_b joins the channel
    http_channel_join(url, user_b["token"], c_id_1)

    # User_b sends a message to the channel
    msg_1 = http_message_send(url, user_b["token"], c_id_1, "Throw it out the window").json()
    m_id_1 = msg_1["message_id"]

    # User_a reacts to user_b's message
    http_message_react(url, user_a["token"], m_id_1, 1)

    # User_a unreacts to user_b's message
    http_message_unreact(url, user_a["token"], m_id_1, 1)

    # User_a checks that the message has been unreacted to
    channel_msgs = http_channel_messages(url, user_a["token"], c_id_1, 0)

    result = channel_msgs.json()
    assert result == {
        "messages": [
            {
                "message_id": m_id_1,
                "u_id": user_b["u_id"],
                "message": "Throw it out the window",
                "time_created": result["messages"][0]["time_created"],
                "reacts": [
                    {
                        "react_id": 1,
                        "u_ids": [],
                        "is_this_user_reacted": False,
                    },
                ],
                "is_pinned": False,
            }
        ],
        "start": 0,
        "end": -1,
    }

    clear()


def test_message_unreact_http_success_multiple_1(url, user_a, user_b, user_c):
    """
    Test 3 - user successfully unreacts to a message, other user's reacts
    should still appear
    User who unreacted calls channel_messages, is_this_user_reacted should be False
    """
    # User_a makes a channel
    channel_1 = http_channels_create(url, user_a["token"], "billionaire records", True).json()
    c_id_1 = channel_1["channel_id"]

    # User_b and user_c join the channel
    http_channel_join(url, user_b["token"], c_id_1)
    http_channel_join(url, user_c["token"], c_id_1)

    # User_b sends a message to the channel
    msg_1 = http_message_send(url, user_b["token"], c_id_1, "Throw it out the window").json()
    m_id_1 = msg_1["message_id"]

    # User_a and user_c react to user_b's message
    http_message_react(url, user_a["token"], m_id_1, 1)
    http_message_react(url, user_c["token"], m_id_1, 1)

    # User_a unreacts to user_b's message
    http_message_unreact(url, user_a["token"], m_id_1, 1)

    # User_a checks that the message has been unreacted to
    channel_msgs = http_channel_messages(url, user_a["token"], c_id_1, 0)

    result = channel_msgs.json()
    assert result == {
        "messages": [
            {
                "message_id": m_id_1,
                "u_id": user_b["u_id"],
                "message": "Throw it out the window",
                "time_created": result["messages"][0]["time_created"],
                "reacts": [
                    {
                        "react_id": 1,
                        "u_ids": [user_c["u_id"]],
                        "is_this_user_reacted": False,
                    },
                ],
                "is_pinned": False,
            }
        ],
        "start": 0,
        "end": -1,
    }

    clear()


def test_message_unreact_http_success_multiple_2(url, user_a, user_b, user_c):
    """
    Test 4 - user successfully unreacts to a message, other user's reacts
    shoudl still appear
    User who did not unreact calls channel_messages, is_this_user_reacted should be True
    """
    # User_a makes a channel
    channel_1 = http_channels_create(url, user_a["token"], "billionaire records", True).json()
    c_id_1 = channel_1["channel_id"]

    # User_b and user_c join the channel
    http_channel_join(url, user_b["token"], c_id_1)
    http_channel_join(url, user_c["token"], c_id_1)

    # User_b sends a message to the channel
    msg_1 = http_message_send(url, user_b["token"], c_id_1, "Throw it out the window").json()
    m_id_1 = msg_1["message_id"]

    # User_a and user_c react to user_b's message
    http_message_react(url, user_a["token"], m_id_1, 1)
    http_message_react(url, user_c["token"], m_id_1, 1)

    # User_a unreacts to user_b's message
    http_message_unreact(url, user_a["token"], m_id_1, 1)

    # User_c checks that the message has been unreacted to
    channel_msgs = http_channel_messages(url, user_c["token"], c_id_1, 0)

    result = channel_msgs.json()
    assert result == {
        "messages": [
            {
                "message_id": m_id_1,
                "u_id": user_b["u_id"],
                "message": "Throw it out the window",
                "time_created": result["messages"][0]["time_created"],
                "reacts": [
                    {
                        "react_id": 1,
                        "u_ids": [user_c["u_id"]],
                        "is_this_user_reacted": True,
                    },
                ],
                "is_pinned": False,
            }
        ],
        "start": 0,
        "end": -1,
    }

    clear()


def test_message_unreact_http_success_multiple_messages(url, user_a, user_b):
    """
    Test 5 - user successfully unreacts to multiple messages
    """
    # User_a makes a channel
    channel_1 = http_channels_create(url, user_a["token"], "billionaire records", True).json()
    c_id_1 = channel_1["channel_id"]

    # User_b joins the channel
    http_channel_join(url, user_b["token"], c_id_1)

    # User_b sends 2 messages to the channel
    msg_1 = http_message_send(url, user_b["token"], c_id_1, "Throw it out the window").json()
    m_id_1 = msg_1["message_id"]

    msg_2 = http_message_send(url, user_b["token"], c_id_1, "I like trains").json()
    m_id_2 = msg_2["message_id"]

    # User_a reacts to both of user_b's messages
    http_message_react(url, user_a["token"], m_id_1, 1)
    http_message_react(url, user_a["token"], m_id_2, 1)

    # User_a unreacts to both of user_b's messages
    http_message_unreact(url, user_a["token"], m_id_1, 1)
    http_message_unreact(url, user_a["token"], m_id_2, 1)

    # User_a checks that both messages have been unreacted
    channel_msgs = http_channel_messages(url, user_a["token"], c_id_1, 0)

    result = channel_msgs.json()
    assert result == {
        "messages": [
            {
                "message_id": m_id_2,
                "u_id": user_b["u_id"],
                "message": "I like trains",
                "time_created": result["messages"][1]["time_created"],
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
                "time_created": result["messages"][0]["time_created"],
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


def test_message_unreact_http_invalid_message_id(url, user_a):
    """
    Test 6 - System Error - User tries to unreact to a message with an
    invalid message_id
    """
    invalid_m_id = 123456

    payload = http_message_unreact(url, user_a["token"], invalid_m_id, 1)

    assert payload.status_code == 400


def test_message_unreact_http_invalid_react_id(url, user_a):
    """
    Test 7 - System Error - User tries to unreact to a message with an
    invalid react_id
    """
    # User_a makes a channel
    channel_1 = http_channels_create(url, user_a["token"], "billionaire records", True).json()
    c_id_1 = channel_1["channel_id"]

    # User_a sends a message to the channel
    msg_1 = http_message_send(url, user_a["token"], c_id_1, "Throw it out the window").json()
    m_id_1 = msg_1["message_id"]

    # User_a reacts to their own message
    http_message_react(url, user_a["token"], m_id_1, 1)

    # User_a tries to unreact to their own message with an invalid react_id
    invalid_react_id = 123456

    payload = http_message_unreact(url, user_a["token"], m_id_1, invalid_react_id)

    assert payload.status_code == 400


def test_message_unreact_http_invalid_inexistent_rect(url, user_a):
    """
    Test 8 - System Error - User tries to unreact to a message that does not
    have an active react
    """
    # User_a makes a channel
    channel_1 = http_channels_create(url, user_a["token"], "billionaire records", True).json()
    c_id_1 = channel_1["channel_id"]

    # User_a sends a message to the channel
    msg_1 = http_message_send(url, user_a["token"], c_id_1, "Throw it out the window").json()
    m_id_1 = msg_1["message_id"]

    # User_a tries to unreact to their own message
    payload = http_message_unreact(url, user_a["token"], m_id_1, 1)

    assert payload.status_code == 400
