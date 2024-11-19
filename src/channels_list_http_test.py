"""
channels_list_http_test.py

Testing that channel_list works with
http implementation
"""


import pytest
import requests
from echo_http_test import url
from conftest_http import user_a, user_b
from http_channel_functions import http_channel_invite
from http_channels_functions import http_channels_list, http_channels_create


def test_channels_list_http_none(url, user_a):
    """
    Test 1 - Listing channels when the user is not in any channel
    """
    # channels_list request should return a dictionary with empty channels
    channel_list = http_channels_list(url, user_a["token"]).json()

    assert channel_list == {"channels": []}


def test_channels_list_http_pub(url, user_a):
    """
    Test 2 - Listing channels when the user is part of a public channel
    """
    # User_a creates a new channel
    channel_1 = http_channels_create(url, user_a["token"], "billionaire records", True).json()
    c_id_1 = channel_1["channel_id"]

    # channels_list request should return a dictionary with the public channel
    # that the user is part of
    channel_list = http_channels_list(url, user_a["token"]).json()

    assert channel_list == {
        "channels": [
            {
                "channel_id": c_id_1,
                "name": "billionaire records",
            },
        ]
    }


def test_channels_list_http_priv(url, user_a, user_b):
    """
    Test 3 - Listing channels when the user is part of a private channel
    """
    # User_a creates a new channel
    channel_1 = http_channels_create(url, user_a["token"], "the cage", False).json()
    c_id_1 = channel_1["channel_id"]

    # User_a invited user_b to channel - user_b becomes authorised
    http_channel_invite(url, user_a["token"], c_id_1, user_b["u_id"])

    # channels_list request should return a dictionary with the private channel
    channel_list = http_channels_list(url, user_b["token"]).json()

    assert channel_list == {
        "channels": [
            {
                "channel_id": c_id_1,
                "name": "the cage",
            },
        ]
    }


def test_channels_list_http_pub_priv(url, user_a, user_b):
    """
    Test 4 - Listing channels when the user is in both
    a public and private channel
    """
    # User_a creates a new public channel
    channel_1 = http_channels_create(url, user_a["token"], "billionaire records", True).json()
    c_id_1 = channel_1["channel_id"]

    # User_a creates a new private channel
    channel_2 = http_channels_create(url, user_a["token"], "the cage", False).json()
    c_id_2 = channel_2["channel_id"]

    # User_a invites user_b to both created channels
    http_channel_invite(url, user_a["token"], c_id_1, user_b["u_id"])
    http_channel_invite(url, user_a["token"], c_id_2, user_b["u_id"])

    # channels_list request should return a dictionary with bot
    # pub and priv channels
    channel_list = http_channels_list(url, user_b["token"]).json()

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


def test_channels_list_http_some(url, user_a, user_b):
    """
    Test 5 - Lists channels that only user_a is considered
    an authorised user for
    """
    # User_a creates a new public channel
    channel_1 = http_channels_create(url, user_a["token"], "billionaire records", True).json()
    c_id_1 = channel_1["channel_id"]

    # User_b creates a new private channel
    http_channels_create(url, user_b["token"], "the cage", False)

    # Channels_list request should return a dictionary the channel user_a is in
    channel_list = http_channels_list(url, user_a["token"]).json()

    assert channel_list == {
        "channels": [
            {
                "channel_id": c_id_1,
                "name": "billionaire records",
            },
        ]
    }


def test_channels_list_http_invalid_token(url):
    """
    Test 6 - System Error - Invalid token passed in
    """
    # Error should occur since token passed is invalid
    invalid_token = ""
    payload = http_channels_list(url, invalid_token)
    assert payload.status_code == 400
