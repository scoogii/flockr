"""
other.py's clear()

Takes in no parameters
Returns an empty dictionary {}

Description: Resets the internal DATA of the application
to its initial state

Exceptions: N/A
"""


import pytest
from auth import auth_register
from channels import channels_create
from data import DATA
from other import clear
from conftest import user_a


def test_clear_channels_only(user_a):
    """
    Test 1 - Testing all added channels are removed from DATA
    """
    # Create channel 1
    channels_create(user_a["token"], "Billionaire Records", True)
    # Create channel 2
    channels_create(user_a["token"], "The Cage", False)

    # Clear channels in channels DATA
    clear()

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


def test_clear_users_only():
    """
    Test 2 - Testing all added users are removed from DATA
    """
    auth_register("nbayoungboy@gmail.com", "youngboynba123", "Kentrell", "Gaulden")
    auth_register("jerrychan@gmail.com", "w89rfh@fk", "Jerry", "Chan")
    auth_register("jamalmuray27@gmail.com", "NuggetsinFive41", "Jamal", "Murray")

    # Clear users in users DATA
    clear()

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
