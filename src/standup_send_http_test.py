"""
standup_send_http_test.py

Testing that message_send works with
http implementation
"""

from time import sleep
import requests
import pytest
from data import DATA
from echo_http_test import url
from conftest_http import user_a, user_b
from http_channel_functions import http_channel_messages
from http_channels_functions import http_channels_create
from http_message_functions import http_message_send
from http_standup_functions import http_standup_start, http_standup_send
from http_user_functions import http_user_profile


def test_standup_send_test_1(url, user_a):
    """
    Test 1 - Standup send success
    """
    # User_a makes a channel
    channel_1 = http_channels_create(url, user_a["token"], "billionaire records", True).json()
    c_id_1 = channel_1["channel_id"]

    # User_a sends a message to the channel
    http_message_send(url, user_a["token"], c_id_1, "/standup 5")

     # Set the standup status
    http_standup_start(url, user_a["token"], c_id_1, 5)

    http_standup_send(url, user_a["token"], c_id_1, "Throw it out the window")

    # Wait 6 seconds
    sleep(6)

    # Get the user's handle
    user_a_profile = http_user_profile(url, user_a["token"], user_a["u_id"]).json()
    user_a_handle = user_a_profile["user"]["handle_str"]

    channel_msgs = http_channel_messages(url, user_a["token"], c_id_1, 0)

    result = channel_msgs.json()
    assert result == {
        "messages": [
            {
                "message_id": 2,
                "u_id": 1,
                "message": f"{user_a_handle}: Throw it out the window\n",
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
            {
                "message_id": 1,
                "u_id": 1,
                "message": "/standup 5",
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



def test_standup_send_http_test_simultaneous(url, user_a):
    """
    Test 2 - Simultaneous standup send success
    """
    # User_a makes a channel
    channel_1 = http_channels_create(url, user_a["token"], "billionaire records", True).json()
    c_id_1 = channel_1["channel_id"]

    # User_a makes another channel
    channel_2 = http_channels_create(url, user_a["token"], "the cage", True).json()
    c_id_2= channel_2["channel_id"]

    # User_a starts a standup in channel 1
    http_standup_start(url, user_a["token"], c_id_1, 5)

    # User_a starts a standup in channel 2
    http_standup_start(url, user_a["token"], c_id_2, 5)

    http_standup_send(url, user_a["token"], c_id_2, "Throw it out the window")

    # Wait 6 seconds
    sleep(6)

    # Get the user's handle
    user_a_profile = http_user_profile(url, user_a["token"], user_a["u_id"]).json()
    user_a_handle = user_a_profile["user"]["handle_str"]

    channel_msgs = http_channel_messages(url, user_a["token"], c_id_2, 0)

    result = channel_msgs.json()
    assert result == {
        "messages": [
            {
                "message_id": 1,
                "u_id": 1,
                "message": f"{user_a_handle}: Throw it out the window\n",
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

def test_standup_send_test_invalid_c_id(url, user_a):
    """
    Test 2 - System Error - Invalid channel ID
    """
    # User_a makes a channel
    channel_1 = http_channels_create(url, user_a["token"], "billionaire records", True).json()
    c_id_1 = channel_1["channel_id"]

    # User_a sends a message to the channel
    http_message_send(url, user_a["token"], c_id_1, "/standup 200")

     # Set the standup status
    http_standup_start(url, user_a["token"], c_id_1, 200)

    invalid_cid = 12345
    payload = http_standup_send(url, user_a["token"], invalid_cid, "Throw it out the window")

    assert payload.status_code == 400


def test_standup_send_test_too_long(url, user_a):
    """
    Test 3 - System Error - Too many characters in message
    """
    # User_a makes a channel
    channel_1 = http_channels_create(url, user_a["token"], "billionaire records", True).json()
    c_id_1 = channel_1["channel_id"]

    # User_a sends a message to the channel
    http_message_send(url, user_a["token"], c_id_1, "/standup 200")

    # Set the standup status
    http_standup_start(url, user_a["token"], c_id_1, 200)

    payload = http_standup_send(url, user_a["token"], c_id_1, "A" * 1001)

    assert payload.status_code == 400


def test_standup_send_test_inactive(url, user_a):
    """
    Test 4 - Standup send raises InputError due to no active standup running
    """
    # User_a makes a channel
    channel_1 = http_channels_create(url, user_a["token"], "billionaire records", True).json()
    c_id_1 = channel_1["channel_id"]

    # User_a sends a message to the channel
    http_message_send(url, user_a["token"], c_id_1, "/standup 200")

    payload = http_standup_send(url, user_a["token"], c_id_1, "Throw it out the window")

    assert payload.status_code == 400


def test_standup_send_test_not_part(url, user_a, user_b):
    """
    Test 4 - Standup send raises InputError due to no active standup running
    """
    # User_a makes a channel
    channel_1 = http_channels_create(url, user_a["token"], "billionaire records", True).json()
    c_id_1 = channel_1["channel_id"]

    # User_a sends a message to the channel
    http_message_send(url, user_a["token"], c_id_1, "/standup 200")

    # Set the standup status
    http_standup_start(url, user_a["token"], c_id_1, 200)

    payload = http_standup_send(url, user_b["token"], c_id_1, "Throw it out the window")

    assert payload.status_code == 400
