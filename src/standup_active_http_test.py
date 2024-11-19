"""
standup_active_http_test.py

Testing that message_send works with
http implementation
"""


import time
import requests
import pytest
from data import DATA
from echo_http_test import url
from conftest_http import user_a, user_b
from standup_active_test import get_time_finish
from http_channels_functions import http_channels_create
from http_standup_functions import http_standup_active, http_standup_start


def test_standup_active_inactive(url, user_a):
    """
    Test 1 - Standup is inactive
    """
    # User_a makes a channel
    channel_1 = http_channels_create(url, user_a["token"], "billionaire records", True).json()
    c_id_1 = channel_1["channel_id"]

    payload = http_standup_active(url, user_a["token"], c_id_1)

    result = payload.json()
    assert result == {
        "is_active": False,
        "time_finish": None,
    }


def test_standup_active_active(url, user_a):
    """
    Test 2 - Standup is active
    """
    # User_a makes a channel
    channel_1 = http_channels_create(url, user_a["token"], "billionaire records", True).json()
    c_id_1 = channel_1["channel_id"]

    http_standup_start(url, user_a["token"], c_id_1, 200)

    payload = http_standup_active(url, user_a["token"], c_id_1)

    result = payload.json()
    assert result["is_active"] == True
    assert result["time_finish"] != None


def test_standup_active_wait(url, user_a):
    """
    Test 3 - Standup wait
    """
    # User_a makes a channel
    channel_1 = http_channels_create(url, user_a["token"], "billionaire records", True).json()
    c_id_1 = channel_1["channel_id"]

    http_standup_start(url, user_a["token"], c_id_1, 2)

    payload1 = http_standup_active(url, user_a["token"], c_id_1).json()

    assert payload1["is_active"] == True
    assert payload1["time_finish"] != None

    # Sleep
    time.sleep(2.5)

    payload2 = http_standup_active(url, user_a["token"], c_id_1).json()

    assert payload2 == {
        "is_active": False,
        "time_finish": None,
    }


def test_standup_active_invalid_c_id(url, user_a):
    """
    Test 4 - Standup fails on an invalid channel_id
    """
    # User_a makes a channel
    http_channels_create(url, user_a["token"], "billionaire records", True)

    invalid_cid = 12345
    payload = http_standup_active(url, user_a["token"], invalid_cid)

    assert payload.status_code == 400


def test_standup_active_invalid_token(url, user_a):
    """
    Test 5 - Standup fails on an invalid token
    """
    # User_a makes a channel
    channel_1 = http_channels_create(url, user_a["token"], "billionaire records", True).json()
    c_id_1 = channel_1["channel_id"]

    invalid_token = ""
    payload = http_standup_active(url, invalid_token, c_id_1)

    assert payload.status_code == 400
