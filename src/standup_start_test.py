"""
standup_start

Takes in (token, channel_id, length)
Returns { time_finish }

Description: For a given channel, start the standup period whereby for the next "length" seconds
if someone calls "standup_send" with a message,
it is buffered during the X second window then at the end of the X second window
a message will be added to the message queue in the channel from the user who started the standup.
X is an integer that denotes the number of seconds that the standup occurs for

Exceptions:
- InputError when any of:
    - Channel ID is not a valid channel
    - An active standup is currently running in this channel

"""


import pytest
import time
from channels import channels_create
from message import message_send
from error import InputError, AccessError
from standup import standup_active, standup_start
from other import clear
from standup_active_test import get_time_finish
from conftest import user_a, user_b, user_c


def test_standup_start_1(user_a):
    """
    Test 1 - Standup start success
    """
    channel_1 = channels_create(user_a["token"], "billionaire records", True)
    c_id_1 = channel_1["channel_id"]

    message_send(user_a["token"], c_id_1, "/standup 200")

    start_status = standup_start(user_a["token"], c_id_1, 200)

    assert start_status == {"time_finish": get_time_finish(c_id_1)}

    clear()


def test_standup_start_2(user_a):
    """
    Test 2 - Standup start success - waiting until standup has finished before starting it again
    """
    channel_1 = channels_create(user_a["token"], "billionaire records", True)
    c_id_1 = channel_1["channel_id"]

    # New standup will be created
    message_send(user_a["token"], c_id_1, "/standup 0.5")
    standup_start(user_a["token"], c_id_1, 0.5)

    time.sleep(1)

    # Standup will be activated 
    message_send(user_a["token"], c_id_1, "/standup 1")
    standup_start(user_a["token"], c_id_1, 1)

    clear()


def test_standup_start_invalid_c_id(user_a):
    """
    Test 2 - Standup start fails on an invalid channel_id
    """
    # User_a makes a channel
    channel_1 = channels_create(user_a["token"], "billionaire records", True)
    c_id_1 = channel_1["channel_id"]

    # User_a sends a message
    message_send(user_a["token"], c_id_1, "/standup 200")

    # User_a runs a standup
    with pytest.raises(InputError):
        invalid_c_id = 12345
        standup_start(user_a["token"], invalid_c_id, 200)

    clear()


def test_standup_start_active_already(user_a):
    """
    Test 3 - Standup start fails on standup already active
    """
    # User_a makes a channel
    channel_1 = channels_create(user_a["token"], "billionaire records", True)
    c_id_1 = channel_1["channel_id"]

    # User_a sends a message
    message_send(user_a["token"], c_id_1, "/standup 100")

    standup_active(user_a["token"], c_id_1)
    standup_start(user_a["token"], c_id_1, 100)

    # Error should be raised since a standup is currently active/running
    with pytest.raises(InputError, match=r"Standup is already running"):
        message_send(user_a["token"], c_id_1, "/standup 200")
        standup_start(user_a["token"], c_id_1, 200)

    clear()


def test_standup_start_invalid_token(user_a):
    """
    Test 4 - Standup start fails on an invalid token
    """
    # User_a makes a channel
    channel_1 = channels_create(user_a["token"], "billionaire records", True)
    c_id_1 = channel_1["channel_id"]

    # User_a sends a message
    message_send(user_a["token"], c_id_1, "/standup 10")

    standup_active(user_a["token"], c_id_1)

    # Error should be raised since token passed in is invalid
    with pytest.raises(AccessError, match=r"Invalid Token"):
        invalid_token = 12345
        standup_active(invalid_token, c_id_1)

    clear()
