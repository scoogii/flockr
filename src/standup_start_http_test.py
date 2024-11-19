"""
standup_start_http_test.py

Testing that message_send works with
http implementation
"""


import time
import requests
import pytest
from data import DATA
from echo_http_test import url
from conftest_http import user_a, user_b
from http_channels_functions import http_channels_create
from http_message_functions import http_message_send
from http_standup_functions import http_standup_active, http_standup_start


def test_standup_start_1(url, user_a):
    """
    Test 1 - Standup start success
    """
    # User_a makes a channel
    channel_1 = http_channels_create(url, user_a["token"], "billionaire records", True).json()
    c_id_1 = channel_1["channel_id"]

    # User_a sends a message to the channel
    http_message_send(url, user_a["token"], c_id_1, "/standup 200")

    # Set the standup status
    payload = http_standup_start(url, user_a["token"], c_id_1, 200).json()

    # Check that a finish_time has been assigned and not equal to None
    assert payload != {
        "time_finish": None,
    }


def test_standup_start_invalid_c_id(url, user_a):
    """
    Test 2 - Standup start fails on an invalid channel_id
    """
    # User_a makes a channel
    channel_1 = http_channels_create(url, user_a["token"], "billionaire records", True).json()
    c_id_1 = channel_1["channel_id"]

    # User_a sends a message to the channel
    http_message_send(url, user_a["token"], c_id_1, "/standup 200")

    # Invalid channel ID
    invalid_c_id = 12345
    payload = http_standup_start(url, user_a["token"], invalid_c_id, 200)

    assert payload.status_code == 400


def test_standup_start_active_already(url, user_a):
    """
    Test 3 - Standup start fails on standup already active
    """
    # User_a makes a channel
    channel_1 = http_channels_create(url, user_a["token"], "billionaire records", True).json()
    c_id_1 = channel_1["channel_id"]

    # User_a sends a message to the channel
    http_message_send(url, user_a["token"], c_id_1, "/standup 200")

     # Set the standup status
    http_standup_start(url, user_a["token"], c_id_1, 100)

    # User_a sends a message to the channel
    http_message_send(url, user_a["token"], c_id_1, "/standup 200")

    payload = http_standup_start(url, user_a["token"], c_id_1, 200)

    assert payload.status_code == 400


def test_standup_start_invalid_token(url, user_a):
    """
    Test 4 - Standup start fails on an invalid token
    """
    # User_a makes a channel
    channel_1 = http_channels_create(url, user_a["token"], "billionaire records", True).json()
    c_id_1 = channel_1["channel_id"]

    # User_a sends a message to the channel
    http_message_send(url, user_a["token"], c_id_1, "/standup 200")

    # Invalid token
    invalid_token = 12345

    payload = http_standup_start(url, invalid_token, c_id_1, 100)

    assert payload.status_code == 400


def test_standup_start_multiple(url, user_a, user_b):
    """
    Test 5 - Can start multiple standups - different finish times exist
    """
    # User_a makes a channel
    channel_1 = http_channels_create(url, user_a["token"], "billionaire records", True).json()
    c_id_1 = channel_1["channel_id"]

    # User_b makes a channel
    channel_2 = http_channels_create(url, user_b["token"], "the cage", True).json()
    c_id_2 = channel_2["channel_id"]

    http_message_send(url, user_a["token"], c_id_1, "/standup 5")
    http_message_send(url, user_b["token"], c_id_2, "/standup 10")

    payload1 = http_standup_start(url, user_a["token"], c_id_1, 1)
    payload2 = http_standup_start(url, user_b["token"], c_id_2, 5)
    
    time.sleep(1.5)

    payload1 = http_standup_active(url, user_a["token"], c_id_1).json()
    assert payload1 == {
        "is_active": False,
        "time_finish": None,
    }

    payload2 = http_standup_active(url, user_b["token"], c_id_2).json()
    assert payload2["is_active"] == True
    assert payload2["time_finish"] != None

def test_standup_restart(url, user_a):
    """
    Test 6 - More than one standup can be run after the previous has finished (tests activate helper)
    """
    # User_a makes a channel
    channel_1 = http_channels_create(url, user_a["token"], "billionaire records", True).json()
    c_id_1 = channel_1["channel_id"]
    
    http_message_send(url, user_a["token"], c_id_1, "/standup 0.5")
    http_standup_start(url, user_a["token"], c_id_1, 0.5)

    time.sleep(1)
    payload1 = http_standup_active(url, user_a["token"], c_id_1).json()
    assert payload1 == {
        "is_active": False,
        "time_finish": None,
    }
    
    http_message_send(url, user_a["token"], c_id_1, "/standup 2")
    http_standup_start(url, user_a["token"], c_id_1, 2)
    payload2 = http_standup_active(url, user_a["token"], c_id_1).json()
    assert payload2["is_active"] == True
    assert payload2["time_finish"] != None
    
