"""
channels_listall_test

Testing that channels_listall works with
http implementation
"""


import pytest
import requests
from echo_http_test import url
from conftest_http import user_a, user_b
from http_channels_functions import (
    http_channels_listall,
    http_channels_create,
)


def test_channels_listall_http_none(url, user_a):
    """
    Test 1 - Listing all channels when no channels exist
    """
    channel_list = http_channels_listall(url, user_a["token"]).json()

    assert channel_list == {"channels": []}


def test_channels_listall_http_same_user(url, user_a):
    """
    Test 2 - Listing all channels when all have been created by same user
    Account for public and private channels
    """
    # User_a makes a channel
    channel_1 = http_channels_create(url, user_a["token"], "billionaire records", True).json()
    c_id_1 = channel_1["channel_id"]

    # Create second channel by the same user
    channel_2 = http_channels_create(url, user_a["token"], "the cage", False).json()
    c_id_2 = channel_2["channel_id"]

    # channels_listall request should return both public and private created channels
    channel_list = http_channels_listall(url, user_a["token"]).json()

    assert channel_list == {
        "channels": [
            {
                "channel_id": c_id_1,
                "name": "billionaire records",
            },
            {
                "channel_id": c_id_2,
                "name": "the cage",
            },
        ]
    }


def test_channels_listall_http_multiple_users(url, user_a, user_b):
    """
    Test 3 - Listing all channels are created by multiple users
    """
    # User_a makes a public channel
    channel_1 = http_channels_create(url, user_a["token"], "billionaire records", True).json()
    c_id_1 = channel_1["channel_id"]

    # User_b makes a private channel
    channel_2 = http_channels_create(url, user_b["token"], "the cage", False).json()
    c_id_2 = channel_2["channel_id"]

    # channels_listall request should return the channels created by both users
    channel_list = http_channels_listall(url, user_a["token"]).json()

    assert channel_list == {
        "channels": [
            {
                "channel_id": c_id_1,
                "name": "billionaire records",
            },
            {
                "channel_id": c_id_2,
                "name": "the cage",
            },
        ]
    }


def test_channels_listall_http_invalid_token(url):
    """
    Test 4 - System Error - Invalid Token passed in
    (refer to assumptions)
    """
    invalid_token = {"token": ""}

    # Error should be raised since token passed is invalid
    payload = requests.get(f"{url}/channels/listall", params=invalid_token)
    assert payload.status_code == 400
