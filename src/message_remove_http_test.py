"""
message_remove_http_test

Testing that message_remove works with
http implementation
"""


import requests
import pytest
from echo_http_test import url
from conftest_http import user_a, user_b, user_c
from http_channel_functions import http_channel_join, http_channel_messages
from http_channels_functions import http_channels_create
from http_message_functions import http_message_send, http_message_remove


def test_message_remove_http_success_admin(url, user_a):
    """
    Test 1 - Test that an admin can successfully remove their own message
    """
    # User_a makes a channel
    channel_1 = http_channels_create(url, user_a["token"], "billionaire records", True).json()
    c_id_1 = channel_1["channel_id"]

    # User_a sends a message to the channel
    msg_1 = http_message_send(url, user_a["token"], c_id_1, "Throw it out the window").json()
    m_id_1 = msg_1["message_id"]

    # User_a removes the message from the channel
    http_message_remove(url, user_a["token"], m_id_1)

    channel_msgs = http_channel_messages(url, user_a["token"], c_id_1, 0)

    result = channel_msgs.json()
    assert result == {
        "messages": [],
        "start": 0,
        "end": -1
    }


def test_message_remove_http_success_owner(url, user_a, user_b):
    """
    Test 2 - Test that an owner can remove another member's message
    """
    # User_b makes a channel
    channel_1 = http_channels_create(url, user_b["token"], "billionaire records", True).json()
    c_id_1 = channel_1["channel_id"]

    # User_a joins the channel
    http_channel_join(url, user_a["token"], c_id_1)

    # User_a sends a message to the channel
    msg_1 = http_message_send(url, user_a["token"], c_id_1, "Throw it out the window").json()
    m_id_1 = msg_1["message_id"]

    # User_b removes the message from the channel
    http_message_remove(url, user_b["token"], m_id_1)

    channel_msgs = http_channel_messages(url, user_a["token"], c_id_1, 0)

    result = channel_msgs.json()
    assert result == {
        "messages": [],
        "start": 0,
        "end": -1
    }


def test_message_remove_http_success_non_admin(url, user_a, user_b):
    """
    Test 3 - Test that a non-admin can successfully remove their own message
    """
    # User_a makes a channel
    channel_1 = http_channels_create(url, user_a["token"], "billionaire records", True).json()
    c_id_1 = channel_1["channel_id"]

    # User_b joins the channel
    http_channel_join(url, user_b["token"], c_id_1)

    # User_b sends a message to the channel
    msg_1 = http_message_send(url, user_b["token"], c_id_1, "Throw it out the window").json()
    m_id_1 = msg_1["message_id"]

    # User_b removes their own message from the channel
    http_message_remove(url, user_b["token"], m_id_1)

    channel_msgs = http_channel_messages(url, user_a["token"], c_id_1, 0)

    result = channel_msgs.json()
    assert result == {
        "messages": [],
        "start": 0,
        "end": -1
    }


def test_message_remove_http_success_admin_other(url, user_a, user_b):
    """
    Test 4 - Test that an admin can remove any other user's message
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

    # User_a removes user_b's messages from the channel
    http_message_remove(url, user_a["token"], m_id_1)
    http_message_remove(url, user_a["token"], m_id_2)

    channel_msgs = http_channel_messages(url, user_a["token"], c_id_1, 0)

    result = channel_msgs.json()
    assert result == {
        "messages": [],
        "start": 0,
        "end": -1
    }


def test_message_remove_http_inexistent_message(url, user_a):
    """
    Test 5 - System Error - Message no longer exists
    """
    # User_a makes a channel
    channel_1 = http_channels_create(url, user_a["token"], "billionaire records", True).json()
    c_id_1 = channel_1["channel_id"]

    # User_a sends a message to the channel
    msg_1 = http_message_send(url, user_a["token"], c_id_1, "Throw it out the window").json()
    m_id_1 = msg_1["message_id"]

    # User_a removes their own message from the channel
    http_message_remove(url, user_a["token"], m_id_1)

    payload = http_message_remove(url, user_a["token"], m_id_1)

    assert payload.status_code == 400


def test_message_remove_invalid_permission_1(url, user_a, user_b):
    """
    Test 6 - System Error - Attempting to remove an admin's message without permissions
    """
    # User_a makes a channel
    channel_1 = http_channels_create(url, user_a["token"], "billionaire records", True).json()
    c_id_1 = channel_1["channel_id"]

    # User_b joins the channel
    http_channel_join(url, user_b["token"], c_id_1)

    # User_a sends a message to the channel
    msg_1 = http_message_send(url, user_a["token"], c_id_1, "Throw it out the window").json()
    m_id_1 = msg_1["message_id"]

    # User_b tries to remove user_a's message from the channel
    payload = http_message_remove(url, user_b["token"], m_id_1)

    assert payload.status_code == 400


def test_message_remove_invalid_permission_2(url, user_a, user_b, user_c):
    """
    Test 7 - System Error - Attempting to remove a user's message without permission
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

    # User_c tries to remove user_b's message from the channel
    payload = http_message_remove(url, user_c["token"], m_id_1)

    assert payload.status_code == 400


def test_message_remove_invalid_permission_3(url, user_a, user_b, user_c):
    """
    Test 8 - System Error - Attempting to remove a user's message without permission
    (not the very first message)
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

    # User_c tries to remove user_b's 2nd message from the channel
    payload = http_message_remove(url, user_c["token"], m_id_2)

    assert payload.status_code == 400


def test_message_remove_http_invalid_token(url, user_a):
    """
    Test 9 - System Error - Invalid token passed in
    """
    # User_a makes a channel
    channel_1 = http_channels_create(url, user_a["token"], "billionaire records", True).json()
    c_id_1 = channel_1["channel_id"]

    # User_a sends a message to the channel
    msg_1 = http_message_send(url, user_a["token"], c_id_1, "Throw it out the window").json()
    m_id_1 = msg_1["message_id"]

    invalid_token = ""
    # User_a tries to remove the message from the channel
    payload = http_message_remove(url, invalid_token, m_id_1)

    assert payload.status_code == 400
