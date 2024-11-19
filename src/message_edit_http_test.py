"""
message_edit_http_test

Testing that message_edit works with
http implementation
"""


import requests
import pytest
from echo_http_test import url
from conftest_http import user_a, user_b, user_c
from http_channel_functions import http_channel_join, http_channel_messages
from http_channels_functions import http_channels_create
from http_message_functions import http_message_send, http_message_edit


def test_message_edit_http_success_own_message(url, user_a):
    """
    Test 1 - user successfully edits their own message
    """
    # User_a makes a channel
    channel_1 = http_channels_create(url, user_a["token"], "billionaire records", True).json()
    c_id_1 = channel_1["channel_id"]

    # User_a sends a message to the channel
    msg_1 = http_message_send(url, user_a["token"], c_id_1, "Throw it out the window").json()
    m_id_1 = msg_1["message_id"]

    # User_a edits their own message
    http_message_edit(url, user_a["token"], m_id_1, "I like trains")

    # Check that the message is edited in the channel
    channel_msgs = http_channel_messages(url, user_a["token"], c_id_1, 0)

    result = channel_msgs.json()
    assert result == {
        "messages": [
            {
                "message_id": m_id_1,
                "u_id": user_a["u_id"],
                "message": "I like trains",
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


def test_message_edit_http_success_owner(url, user_b, user_c):
    """
    Test 2 - Owner of channel successfully edits someone else's message
    """
    # User_b makes a channel
    channel_1 = http_channels_create(url, user_b["token"], "billionaire records", True).json()
    c_id_1 = channel_1["channel_id"]

    # User_c joins the channel
    http_channel_join(url, user_c["token"], c_id_1)

    # User_c sends a message to the channel
    msg_1 = http_message_send(url, user_c["token"], c_id_1, "Throw it out the window").json()
    m_id_1 = msg_1["message_id"]

    # User_b edits user_c's message
    http_message_edit(url, user_b["token"], m_id_1, "I like trains")

    # Check that the message is edited in the channel
    channel_msgs = http_channel_messages(url, user_b["token"], c_id_1, 0)

    result = channel_msgs.json()
    assert result == {
        "messages": [
            {
                "message_id": m_id_1,
                "u_id": user_c["u_id"],
                "message": "I like trains",
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


def test_message_edit_http_success_admin(url, user_a, user_b):
    """
    Test 3 - Admin successfully edits someone else's message
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

    # User_a edits user_b's 2nd message
    http_message_edit(url, user_a["token"], m_id_2, "My name Jeff")

    # Check that the message is edited in the channel
    channel_msgs = http_channel_messages(url, user_a["token"], c_id_1, 0)

    result = channel_msgs.json()
    assert result == {
        "messages": [
            {
                "message_id": m_id_2,
                "u_id": user_b["u_id"],
                "message": "My name Jeff",
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
                "is_pinned": False,
            },
        ],
        "start": 0,
        "end": -1,
    }


def test_message_edit_http_success_empty(url, user_a):
    """
    Test 4 - User updates message with empty string (message is deleted)
    """
    # User_a makes a channel
    channel_1 = http_channels_create(url, user_a["token"], "billionaire records", True).json()
    c_id_1 = channel_1["channel_id"]

    # User_a sends a message to the channel
    msg_1 = http_message_send(url, user_a["token"], c_id_1, "Throw it out the window").json()
    m_id_1 = msg_1["message_id"]

    # User_a edits their own message
    http_message_edit(url, user_a["token"], m_id_1, "")

    # Check that the message is edited in the channel
    channel_msgs = http_channel_messages(url, user_a["token"], c_id_1, 0)

    result = channel_msgs.json()
    assert result == {
        "messages": [],
        "start": 0,
        "end": -1,
    }


def test_message_edit_http_invalid_permission_1(url, user_a, user_b):
    """
    Test 5 - System Error - User tries to edit someone else's message
    but is not an admin/owner while the other person is an owner
    """
    # User_a makes a channel
    channel_1 = http_channels_create(url, user_a["token"], "billionaire records", True).json()
    c_id_1 = channel_1["channel_id"]

    # User_b joins the channel
    http_channel_join(url, user_b["token"], c_id_1)

    # User_a sends a message to the channel
    msg_1 = http_message_send(url, user_a["token"], c_id_1, "Throw it out the window").json()
    m_id_1 = msg_1["message_id"]

    # User_b tries to edit user_a's message
    payload = http_message_edit(url, user_b["token"], m_id_1, "I like trains")

    assert payload.status_code == 400


def test_message_edit_http_invalid_permission_2(url, user_a, user_b, user_c):
    """
    Test 6 - System Error - User tries to edit someone else's message but is
    not an admin/owner while the other person also is not
    """
    # User_a makes a channel
    channel_1 = http_channels_create(url, user_a["token"], "billionaire records", True).json()
    c_id_1 = channel_1["channel_id"]

    # User_b joins the channel
    http_channel_join(url, user_b["token"], c_id_1)
    # User_c joins the channel
    http_channel_join(url, user_c["token"], c_id_1)

    # User_b sends a message to the channel
    msg_1 = http_message_send(url, user_b["token"], c_id_1, "Throw it out the window").json()
    m_id_1 = msg_1["message_id"]

    # User_c tries to edit user_b's message
    payload = http_message_edit(url, user_c["token"], m_id_1, "I like trains")

    assert payload.status_code == 400


def test_message_edit_http_invalid_permission_3(url, user_a, user_b, user_c):
    """
    Test 7 - System Error - User tries to edit someone else's message but is
    not an admin/owner while the other person also is not (not first message)
    """
    # User_a makes a channel
    channel_1 = http_channels_create(url, user_a["token"], "billionaire records", True).json()
    c_id_1 = channel_1["channel_id"]

    # User_b joins the channel
    http_channel_join(url, user_b["token"], c_id_1)
    # User_c joins the channel
    http_channel_join(url, user_c["token"], c_id_1)

    # User_b sends 3 messages to the channel
    http_message_send(url, user_b["token"], c_id_1, "Throw it out the window")

    msg_2 = http_message_send(url, user_b["token"], c_id_1, "I like trains").json()
    m_id_2 = msg_2["message_id"]

    http_message_send(url, user_b["token"], c_id_1, "My name Jeff")

    # User_c tries to edit user_b's 2nd message
    payload = http_message_edit(url, user_c["token"], m_id_2, "My name Jeff")

    assert payload.status_code == 400


def test_message_edit_http_invalid_token(url, user_a):
    """
    Test 8 - System Error - Invalid token passed in
    """
    # User_a makes a channel
    channel_1 = http_channels_create(url, user_a["token"], "billionaire records", True).json()
    c_id_1 = channel_1["channel_id"]

    # User_a sends a message to the channel
    msg_1 = http_message_send(url, user_a["token"], c_id_1, "Throw it out the window").json()
    m_id_1 = msg_1["message_id"]

    invalid_token = ""
    # User_a tries to edit their own message
    payload = http_message_edit(url, invalid_token, m_id_1, "I like trains")

    assert payload.status_code == 400


def test_message_edit_http_edit_too_long(url, user_a):
    """
    Test 9 - System Error - User tries to edit a message that is >
    1000 characters
    """
    # User_a makes a channel
    channel_1 = http_channels_create(url, user_a["token"], "billionaire records", True).json()
    c_id_1 = channel_1["channel_id"]

    # User_a sends a message to the channel
    msg_1 = http_message_send(url, user_a["token"], c_id_1, "Throw it out the window").json()
    m_id_1 = msg_1["message_id"]

    # User_a tries to edit their own message
    payload = http_message_edit(url, user_a["token"], m_id_1, "a" * 1001)

    assert payload.status_code == 400
