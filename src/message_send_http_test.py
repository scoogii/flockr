"""
message_send_http_test

Testing that message_send works with
http implementation
"""


import requests
import pytest
from data import DATA
from echo_http_test import url
from conftest_http import user_a, user_b
from http_channel_functions import http_channel_messages
from http_channels_functions import http_channels_create
from http_message_functions import http_message_send


def test_message_send_http_success(url, user_a):
    """
    Test 1 - message is successfully sent by the
    authorised used to the channel
    """
    # User_a makes a channel
    channel_1 = http_channels_create(url, user_a["token"], "billionaire records", True).json()
    c_id_1 = channel_1["channel_id"]

    # User_a sends a message to the channel
    msg_1 = http_message_send(url, user_a["token"], c_id_1, "Throw it out the window").json()
    m_id_1 = msg_1["message_id"]

    # Check that the message is in the channel
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
                    }
                ],
                "is_pinned": False,
            }
        ],
        "start": 0,
        "end": -1,
    }


def test_message_send_http_multiple(url, user_a):
    """
    Test 2 - message is successfully sent by the
    authorised user to the channel
    """
    # User_a makes a channel
    channel_1 = http_channels_create(url, user_a["token"], "billionaire records", True).json()
    c_id_1 = channel_1["channel_id"]

    # User_a sends multiple messages to the channel
    msg_1 = http_message_send(url, user_a["token"], c_id_1, "Throw it out the window").json()
    m_id_1 = msg_1["message_id"]

    msg_2 = http_message_send(url, user_a["token"], c_id_1, "I like trains").json()
    m_id_2 = msg_2["message_id"]

    msg_3 = http_message_send(url, user_a["token"], c_id_1, "My name Jeff").json()
    m_id_3 = msg_3["message_id"]

    # Check that the message is in the channel
    channel_msgs = http_channel_messages(url, user_a["token"], c_id_1, 0)

    result = channel_msgs.json()
    assert result == {
        "messages": [
            {
                "message_id": m_id_3,
                "u_id": user_a["u_id"],
                "message": "My name Jeff",
                "time_created": result["messages"][2]["time_created"],
                "reacts": [
                    {
                        "react_id": 1,
                        "u_ids": [],
                        "is_this_user_reacted": False,
                    }
                ],
                "is_pinned": False,
            },
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
                "is_pinned": False,
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
                "is_pinned": False,
            },
        ],
        "start": 0,
        "end": -1,
    }


def test_message_send_http_too_long(url, user_a):
    """
    Test 3 - System Error - Message is > 1000 characters
    Assumes user is authorised and can join the channel
    """
    # User_a makes a channel
    channel_1 = http_channels_create(url, user_a["token"], "billionaire records", True).json()
    c_id_1 = channel_1["channel_id"]

    payload = http_message_send(url, user_a["token"], c_id_1, "a" * 1001)

    assert payload.status_code == 400


def test_message_send_http_too_short(url, user_a):
    """
    Test 4 - System Error - Message is < 1 character
    Assumes user is authorised and can join the channel
    """
    # User_a makes a channel
    channel_1 = http_channels_create(url, user_a["token"], "billionaire records", True).json()
    c_id_1 = channel_1["channel_id"]

    payload = http_message_send(url, user_a["token"], c_id_1, "a" * 0)

    assert payload.status_code == 400


def test_message_send_http_not_in_channel(url, user_a, user_b):
    """
    Test 5 - System Error - User is NOT a part of the channel
    and tries to send a message
    """
    # User_a makes a channel
    channel_1 = http_channels_create(url, user_a["token"], "billionaire records", True).json()
    c_id_1 = channel_1["channel_id"]

    payload = http_message_send(url, user_b["token"], c_id_1, "Throw it out the window")

    assert payload.status_code == 400


def test_message_send_http_invalid_token(url, user_a):
    """
    Test 6 - System Error - Invalid token passed in
    """
    # User_a makes a channel
    channel_1 = http_channels_create(url, user_a["token"], "billionaire records", True).json()
    c_id_1 = channel_1["channel_id"]

    invalid_token = ""

    payload = http_message_send(url, invalid_token, c_id_1, "Throw it out the window")

    assert payload.status_code == 400
