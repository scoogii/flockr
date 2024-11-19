"""
message_sendlist

Takes in parameters `token`, `channel_id`, `message`, `time_sent`
Returns a dictionary {message_id}

Description: Sends a message from authorised_user to the channel
specified by channel_id automatically at a specified time in the
future

Exceptions:
  - InputError when any of:
    - Channel ID is not a valid channel
    - Message is more than 1000 characters
    - Time sent is a time in the past
  - AccessError when the authorised user has not joined they channel
  they are trying to post to
"""


from datetime import datetime
from time import sleep
import pytest
from auth import auth_register
from channel import channel_messages
from channels import channels_create
from data import DATA
from error import AccessError, InputError
from message import message_send, message_sendlater
from other import clear
from conftest import user_a, user_b


def get_time_created(m_id):
    """
    Retrieves the time_created for a message given a message_id
    """
    for message in DATA["message_log"]["messages"]:
        if m_id == message["message_id"]:
            return message["time_created"]


def test_message_sendlater_success_m_id(user_a):
    """
    Test 1 - Testing that the function successfully returns the correct
    message_id when sent later
    """
    # User_a makes a channel
    channel_1 = channels_create(user_a["token"], "billionaire records", True)
    c_id_1 = channel_1["channel_id"]

    # User_a makes a request to send a message in 5 seconds
    message = "Throw it out the window"
    time_in_5 = int((datetime.now()).timestamp()) + 5
    msg_1 = message_sendlater(user_a["token"], c_id_1, message, time_in_5)

    assert msg_1["message_id"] == 1

    # Wait for message to send then clear
    sleep(7)
    clear()


def test_message_sendlater_success_sent(user_a):
    """
    Test 2 - Testing that the function successfully sends a message
    in the future
    """
    # User_a makes a channel
    channel_1 = channels_create(user_a["token"], "billionaire records", True)
    c_id_1 = channel_1["channel_id"]

    # User_a makes a request to send a message in 5 seconds
    message = "Throw it out the window"
    time_in_5 = int((datetime.now()).timestamp()) + 5
    message_sendlater(user_a["token"], c_id_1, message, time_in_5)

    # Wait 7 seconds
    sleep(7)

    # Check if message was successfully sent later
    assert channel_messages(user_a["token"], c_id_1, 0) == {
        "messages": [
            {
                "message_id": 1,
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

    clear()


def test_message_sendlater_double_success(user_a):
    """
    Test 3 - Tests that user sending two of the same messages later
    is successful
    """
    # User_a makes a channel
    channel_1 = channels_create(user_a["token"], "billionaire records", True)
    c_id_1 = channel_1["channel_id"]

    # User_a makes a request to send a message in 5 seconds
    message_1 = "Throw it out the window"
    time_in_5 = int((datetime.now()).timestamp()) + 5
    message_sendlater(user_a["token"], c_id_1, message_1, time_in_5)

    # User_a makes another request to send a message in 6 seconds
    message_2 = "I like trains"
    time_in_6 = time_in_5 + 1
    message_sendlater(user_a["token"], c_id_1, message_2, time_in_6)

    # Wait for 10 seconds
    sleep(10)

    # Check if the two messages were successfully sent later
    assert channel_messages(user_a["token"], c_id_1, 0) == {
        "messages": [
            {
                "message_id": 2,
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
                "message_id": 1,
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

    clear()

def test_message_sendlater_mix(user_a):
    """
    Test 4 - Tests that a message being sent in between will still
    let sendlater work successfully
    """
    # User_a makes a channel
    channel_1 = channels_create(user_a["token"], "billionaire records", True)
    c_id_1 = channel_1["channel_id"]

    # User_a makes a request to send a message in 5 seconds
    message_1 = "Throw it out the window"
    time_in_5 = int((datetime.now()).timestamp()) + 5
    message_sendlater(user_a["token"], c_id_1, message_1, time_in_5)

    # User_a makes another request to send a message immediately
    message_2 = "I like trains"
    msg_2 = message_send(user_a["token"], c_id_1, message_2)
    m_id_2 = msg_2["message_id"]

    # Wait 7 seconds
    sleep(7)

    # Check that both messages are sent successfully and in the right order
    assert channel_messages(user_a["token"], c_id_1, 0) == {
        "messages": [
            {
                "message_id": 1,
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
                "message_id": 2,
                "u_id": user_a["u_id"],
                "message": "I like trains",
                "time_created": get_time_created(m_id_2),
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

    clear()


def test_message_sendlater_invalid_cid(user_a):
    """
    Test 5 - InputError - for invalid channel ID
    """
    # Create an invalid channel ID
    invalid_c_id = 4566343
    message = "Throw it out the window"
    time_in_5 = int((datetime.now()).timestamp()) + 5
    # User_a cannot send a message later because channel ID is invalid
    with pytest.raises(InputError):
        # User_a makes a request to send a message in 5 seconds
        message_sendlater(user_a["token"], invalid_c_id, message, time_in_5)

    clear()


def test_message_sendlater_message_long(user_a):
    """
    Test 6 - InputError - Message is > 1000 characters
    """
    # User_a makes a channel
    channel_1 = channels_create(user_a["token"], "billionaire records", True)
    c_id_1 = channel_1["channel_id"]

    # Message is invalid since it is greater than 1000 characters
    time_in_5 = int((datetime.now()).timestamp()) + 5
    with pytest.raises(InputError, match=r"Messages should be between 0 and 1000 characters long"):
        message_sendlater(user_a["token"], c_id_1, "A" * 1001, time_in_5)

    clear()


def test_message_sendlater_past(user_a):
    """
    Test 7 - InputError - Time to be sent at is a time in the past
    """
    # User_a makes a channel
    channel_1 = channels_create(user_a["token"], "billionaire records", True)
    c_id_1 = channel_1["channel_id"]

    message = "Throw it out the window"
    time_past = 0

    # Message is invalid since the time to be sent later is in the past
    with pytest.raises(InputError, match=r"Left bound is greater than the right bound"):
        message_sendlater(user_a["token"], c_id_1, message, time_past)

    clear()


def test_message_sendlater_unauth(user_a, user_b):
    """
    Test 8 - AccessError - The authorised user has not joined the
    channel they are trying to post to
    """
    # User_a makes a channel
    channel_1 = channels_create(user_a["token"], "billionaire records", True)
    c_id_1 = channel_1["channel_id"]

    message = "Throw it out the window"
    time_in_5 = int((datetime.now()).timestamp()) + 5

    # User_b attempts to send a message later to a channel they are part of
    with pytest.raises(AccessError, match=r"You must be a member of the channel to view its details"):
        message_sendlater(user_b["token"], c_id_1, message, time_in_5)

    clear()
