"""
other.py's clear()

Takes in no parameters
Returns an empty dictionary {}

Description: Resets the internal DATA of the application
to its initial state

Exceptions: N/A
"""


import pytest
import requests
from echo_http_test import url
from conftest_http import user_a, user_b, user_c
from data import DATA
from http_auth_functions import http_auth_register
from http_channels_functions import http_channels_create, http_channels_listall
from http_message_functions import http_message_send
from http_other_functions import http_clear, http_users_all


def test_clear_users_all(url, user_a, user_b, user_c):
    """
    Test 1 - Success - check that three users are registered and cleared
    """
    # Clear the three users that were registered
    http_clear(url)

    # Register a new user
    email = "jeffsmithiscool@gmail.com"
    password = "smithjeff"
    name_first = "Jeff"
    name_last = "Smith"

    payload = http_auth_register(url, email, password, name_first, name_last)
    user_d = payload.json()

    # With user_d token -> Request users_all data
    payload = http_users_all(url, user_d["token"])
    profile = payload.json()

    # The only user in data should be user_d
    assert profile == {
        'users': [
            {
                'u_id': 1,
                'email': 'jeffsmithiscool@gmail.com',
                'name_first': 'Jeff',
                'name_last': 'Smith',
                'handle_str': 'jeffsmith',
                'profile_img_url': None,
            }
        ]
    }

def test_clear_channels(url, user_a):
    """
    Test 2 - Success - check that three users are registered and cleared
    """
    # MAKE TWO CHANNELS
    http_channels_create(url, user_a["token"], "billionaire records", True)
    http_channels_create(url, user_a["token"], "the cage", False)

    # CLEAR DATA
    http_clear(url)

    # Register a new user to get a token
    email = "jeffsmithiscool@gmail.com"
    password = "smithjeff"
    name_first = "Jeff"
    name_last = "Smith"

    payload = http_auth_register(url, email, password, name_first, name_last)
    user_d = payload.json()

    # Check there are no channels
    payload = http_channels_listall(url, user_d["token"])

    result = payload.json()
    assert result == {"channels": []}


def test_clear_data(url, user_a):
    """
    Test 3 - Success - check using the data structure that users, channels and messages are clear
    """
    # User_a makes a channel
    channel_1 = http_channels_create(url, user_a["token"], "billionaire records", True).json()
    c_id_1 = channel_1["channel_id"]

    # User_a sends a message to the channel
    http_message_send(url, user_a["token"], c_id_1, "Throw it out the window")

    # CLEAR DATA
    http_clear(url)

    # DATA should be empty
    assert DATA == {
        "channels": [],
        "users": [],
        "message_log":
            {
                "messages": [],
                "msg_counter": 1,
            },
        "standup": []
    }
