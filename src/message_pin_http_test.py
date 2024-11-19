"""
message_pin_test

Teting that message_pin works with
http implementation
"""


import requests
from echo_http_test import url
from conftest_http import user_a, user_b
from http_channel_functions import http_channel_join, http_channel_messages
from http_channels_functions import http_channels_create
from http_message_functions import http_message_send, http_message_pin


def test_message_pin_http_success(url, user_a, user_b):
    """
    Test 1 - Message is successfully pinned by the owner of the channel
    """
    # User_a makes a channel
    channel_1 = http_channels_create(url, user_a["token"], "billionaire records", True).json()
    c_id_1 = channel_1["channel_id"]

    # User_b joins and sends a message
    http_channel_join(url, user_b["token"], c_id_1)

    msg_1 = http_message_send(url, user_b["token"], c_id_1, "Throw it out the window").json()
    m_id_1 = msg_1["message_id"]

    # User_a pins the message
    http_message_pin(url, user_a["token"], m_id_1)

    # Check that the message has been pinned successfully
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
                    }
                ],
                "is_pinned": True,
            }
        ],
        "start": 0,
        "end": -1,
    }


def test_message_pin_http_multiple(url, user_a):
    """
    Test 2 - Testing that pinning multiple messages is successful
    """
    # User_a makes a channel
    channel_1 = http_channels_create(url, user_a["token"], "billionaire records", True).json()
    c_id_1 = channel_1["channel_id"]

    # User_a sends a message
    msg_1 = http_message_send(url, user_a["token"], c_id_1, "Throw it out the window").json()
    m_id_1 = msg_1["message_id"]

    # User_a sends another message
    msg_2 = http_message_send(url, user_a["token"], c_id_1, "I like trains").json()
    m_id_2 = msg_2["message_id"]


    # User_a pins both messages
    http_message_pin(url, user_a["token"], m_id_1)

    http_message_pin(url, user_a["token"], m_id_2)

    # Check that the messages have been pinned successfully
    channel_msgs = http_channel_messages(url, user_a["token"], c_id_1, 0)

    result = channel_msgs.json()
    assert result == {
        "messages": [
            {
                "message_id": m_id_2,
                "u_id": user_a["u_id"],
                "message": "I like trains",
                "time_created": result["messages"][1]["time_created"],
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
                "message_id": m_id_1,
                "u_id": user_a["u_id"],
                "message": "Throw it out the window",
                "time_created": result["messages"][0]["time_created"],
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


def test_message_pin_http_invalid_mid(url, user_a):
    """
    Test 3 - System Error - Pinning a message with an invalid message_id
    """
    # User_a makes a channel
    http_channels_create(url, user_a["token"], "billionaire records", True).json()

    # Message is invalid since message_id does not belong to an existing message
    invalid_m_id = 4566343
    payload = http_message_pin(url, user_a["token"], invalid_m_id)

    assert payload.status_code == 400


def test_message_pin_http_already_pinned(url, user_a, user_b):
    """
    Test 4 - System Error - Pinning a message that is already pinned
    """
    # User_a makes a channel
    channel_1 = http_channels_create(url, user_a["token"], "billionaire records", True).json()
    c_id_1 = channel_1["channel_id"]


    # User_b joins and sends a message
    http_channel_join(url, user_b["token"], c_id_1)

    msg_1 = http_message_send(url, user_a["token"], c_id_1, "Throw it out the window").json()
    m_id_1 = msg_1["message_id"]

    # User_a pins the message
    http_message_pin(url, user_a["token"], m_id_1)

    # System error should occur since the message has already been pinned
    payload = http_message_pin(url, user_a["token"], m_id_1)

    assert payload.status_code == 400


def test_message_pin_http_not_in_channel(url, user_a, user_b):
    """
    Test 5 - System Error - Pinning a message when user is not in the channel
    """
    # User_a makes a channel
    channel_1 = http_channels_create(url, user_a["token"], "billionaire records", True).json()
    c_id_1 = channel_1["channel_id"]

    # User_a sends a message
    msg_1 = http_message_send(url, user_a["token"], c_id_1, "Throw it out the window").json()
    m_id_1 = msg_1["message_id"]

    # System error should occur since user_b isn't part of the channel the message was sent in
    payload = http_message_pin(url, user_b["token"], m_id_1)

    assert payload.status_code == 400


def test_message_pin_http_unauth(url, user_a, user_b):
    """
    Test 6 - System Error - Pinning a message when the user is not an owner/admin
    """
    # User_a makes a channel
    channel_1 = http_channels_create(url, user_a["token"], "billionaire records", True).json()
    c_id_1 = channel_1["channel_id"]

    # User_a sends a message
    msg_1 = http_message_send(url, user_a["token"], c_id_1, "Throw it out the window").json()
    m_id_1 = msg_1["message_id"]

    # User_b joins the channel
    http_channel_join(url, user_b["token"], c_id_1)

    # System error should occur since user_b is not an owner of the channel or a flockr admin
    payload = http_message_pin(url, user_b["token"], m_id_1)

    assert payload.status_code == 400
