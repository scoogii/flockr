"""
message_sendlater_http

Testing that message_sendlater works with
http implementation
"""


from datetime import datetime
from time import sleep
import requests
from data import DATA
from echo_http_test import url
from conftest_http import user_a, user_b
from http_channel_functions import http_channel_messages
from http_channels_functions import http_channels_create
from http_message_functions import http_message_sendlater, http_message_send


def test_message_sendlater_http_success_m_id(url, user_a):
    """
    Test 1 - Testing that the function successfully returns the correct
    message_id when sent later
    """
    # User_a makes a channel
    channel_1 = http_channels_create(url, user_a["token"], "billionaire records", True).json()
    c_id_1 = channel_1["channel_id"]

    # User_a makes a request to send a message in 5 seconds
    time_in_5 = int((datetime.now()).timestamp()) + 5

    payload = http_message_sendlater(url, user_a["token"], c_id_1, "Throw it out the window",
                                     time_in_5)

    result = payload.json()
    assert result == {"message_id": 1}


def test_message_sendlater_http_success_sent(url, user_a):
    """
    Test 2 - Testing that the function sucessfully sends a message
    in the future
    """
    # User_a makes a channel
    channel_1 = http_channels_create(url, user_a["token"], "billionaire records", True).json()
    c_id_1 = channel_1["channel_id"]

    # User_a makes a request to send a message in 5 seconds
    time_in_5 = int((datetime.now()).timestamp()) + 5

    msg_1 = http_message_sendlater(url, user_a["token"], c_id_1, "Throw it out the window",
                                   time_in_5).json()
    m_id_1 = msg_1["message_id"]

    # Wait 7 seconds
    sleep(7)

    # Check if message was successfully sent later
    channel_msgs = http_channel_messages(url, user_a["token"], c_id_1, 0)

    result = channel_msgs.json()
    assert result == {
        "messages": [
            {
                "message_id": m_id_1,
                "u_id": user_a["u_id"],
                "message": "Throw it out the window",
                "time_created": time_in_5,
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


def test_message_sendlater_http_back_to_back(url, user_a):
    """
    Test 3 - Tests that user sending two of the same messages later
    is successful
    """
    # User_a makes a channel
    channel_1 = http_channels_create(url, user_a["token"], "billionaire records", True).json()
    c_id_1 = channel_1["channel_id"]

    # User_a makes a request to send a message in 5 seconds
    time_in_5 = int((datetime.now()).timestamp()) + 5
    msg_1 = http_message_sendlater(url, user_a["token"], c_id_1, "Throw it out the window",
                                   time_in_5).json()
    m_id_1 = msg_1["message_id"]

    # User_a makes another request to send a message in 6 seconds
    time_in_6 = time_in_5 + 1
    msg_2 = http_message_sendlater(url, user_a["token"], c_id_1, "I like trains", time_in_6).json()
    m_id_2 = msg_2["message_id"]

    # Wait 7 seconds
    sleep(7)

    # Check if the two messages were successfully sent later
    channel_msgs = http_channel_messages(url, user_a["token"], c_id_1, 0)

    result = channel_msgs.json()
    assert result == {
        "messages": [
            {
                "message_id": m_id_2,
                "u_id": user_a["u_id"],
                "message": "I like trains",
                "time_created": time_in_6,
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
                "time_created": time_in_5,
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


def test_message_sendlater_http_mix(url, user_a):
    """
    Test 4 - Tests that a message being sent in between will still
    let sendlater work successfully
    """
    # User_a makes a channel
    channel_1 = http_channels_create(url, user_a["token"], "billionaire records", True).json()
    c_id_1 = channel_1["channel_id"]

    # User_a makes a request to send a message in 5 seconds
    time_in_5 = int((datetime.now()).timestamp()) + 5

    msg_1 = http_message_sendlater(url, user_a["token"], c_id_1, "Throw it out the window"
                                   , time_in_5).json()
    m_id_1 = msg_1["message_id"]

    # User_a makes another request to send a message immediately
    msg_2 = http_message_send(url, user_a["token"], c_id_1, "I like trains").json()
    m_id_2 = msg_2["message_id"]

    # Wait 7 seconds
    sleep(7)

    # Check if the two messages were successfully sent later
    channel_msgs = http_channel_messages(url, user_a["token"], c_id_1, 0)

    result = channel_msgs.json()
    assert result == {
        "messages": [
            {
                "message_id": m_id_1,
                "u_id": user_a["u_id"],
                "message": "Throw it out the window",
                "time_created": time_in_5,
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
        ],
        "start": 0,
        "end": -1,
    }


def test_message_sendlater_http_invalid_cid(url, user_a):
    """
    Test 5 - System Error - for invalid channel ID
    """
    # Create an invalid channel ID
    invalid_c_id = 4566343

    # User_a cannot send a message later because channel ID is invalid
    payload = http_message_sendlater(url, user_a["token"], invalid_c_id, "Throw it out the window",
                                     int((datetime.now()).timestamp()))

    assert payload.status_code == 400


def test_message_sendlater_http_message_long(url, user_a):
    """
    Test 6 - System Error - Message is > 1000 characters
    """
    # User_a makes a channel
    channel_1 = http_channels_create(url, user_a["token"], "billionaire records", True).json()
    c_id_1 = channel_1["channel_id"]

    # Message is invalid since it is greater than 1000 characters
    payload = http_message_sendlater(url, user_a["token"], c_id_1, "A" * 1001,
                                     int((datetime.now()).timestamp()))

    assert payload.status_code == 400


def test_message_sendlater_http_message_past(url, user_a):
    """
    Test 7 - System Error - Time to be sent at is a time in the past
    """
    # User_a makes a channel
    channel_1 = http_channels_create(url, user_a["token"], "billionaire records", True).json()
    c_id_1 = channel_1["channel_id"]

    # Message is invalid since the time to be sent later is in the past
    payload = http_message_sendlater(url, user_a["token"], c_id_1, "Throw it out the window", 0)

    assert payload.status_code == 400


def test_message_sendlater_http_unauth(url, user_a, user_b):
    """
    Test 8 - System Error - The authorised user has not joined the
    channel they are trying to post to
    """
    # User_a makes a channel
    channel_1 = http_channels_create(url, user_a["token"], "billionaire records", True).json()
    c_id_1 = channel_1["channel_id"]

    # User_b attempts to send a message later to a channel they are not part of
    payload = http_message_sendlater(url, user_b["token"], c_id_1, "Throw it out the window",
                                     int((datetime.now()).timestamp()))

    assert payload.status_code == 400
