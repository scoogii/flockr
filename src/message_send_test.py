"""
message_send

Takes in parameters `token`, `channel_id`, `message`
Returns a dictionary {message_id}

Description: Send a message from authorised_user to the
channel specified by the channel_id

Exceptions:
 - InputError: Message > 1000 characters
 - AccessError: Authorised user has not joined channel they are trying to post to

"""


import pytest
from auth import auth_register
from channel import channel_messages
from channels import channels_create
from data import DATA
from error import InputError, AccessError
from message import message_send
from other import clear
from conftest import user_a, user_b


def get_time_created(m_id):
    """
    Retrieves the time_created for a message given a message_id
    """
    for message in DATA["message_log"]["messages"]:
        if m_id == message["message_id"]:
            return message["time_created"]


def test_message_send_success(user_a):
    """
    Test 1 - message is successfully sent by the
    authorised user to the channel
    """
    # User_a creates a channel and automatically joins the channel
    channel_1 = channels_create(user_a["token"], "billionaire records", True)
    c_id_1 = channel_1["channel_id"]

    # Send the message to the channel
    msg_1 = message_send(user_a["token"], c_id_1, "Throw it out the window")
    m_id_1 = msg_1["message_id"]

    # Check that the message is in the channel
    assert channel_messages(user_a["token"], c_id_1, 0) == {
        "messages": [
            {
                "message_id": m_id_1,
                "u_id": user_a["u_id"],
                "message": "Throw it out the window",
                "time_created": get_time_created(m_id_1),
                "reacts": [
                    {
                        "react_id": 1,
                        "u_ids": [],
                        "is_this_user_reacted": False,
                    }
                ],
                "is_pinned": False,
            }
        ],
        "start": 0,
        "end": -1,
    }

    clear()


def test_message_send_success_multiple(user_a):
    """
    Test 2 - message is successfully sent by the
    authorised user to the channel
    """
    # User_a creates a channel and automatically joins the channel
    channel_1 = channels_create(user_a["token"], "billionaire records", True)
    c_id_1 = channel_1["channel_id"]

    # Send three message to the channel
    msg_1 = message_send(user_a["token"], c_id_1, "Throw it out the window")
    m_id_1 = msg_1["message_id"]

    msg_2 = message_send(user_a["token"], c_id_1, "I like trains")
    m_id_2 = msg_2["message_id"]

    msg_3 = message_send(user_a["token"], c_id_1, "My name Jeff")
    m_id_3 = msg_3["message_id"]

    # Check that the message is in the channel
    assert channel_messages(user_a["token"], c_id_1, 0) == {
        "messages": [
            {
                "message_id": m_id_3,
                "u_id": user_a["u_id"],
                "message": "My name Jeff",
                "time_created": get_time_created(m_id_3),
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
            {
                "message_id": m_id_1,
                "u_id": user_a["u_id"],
                "message": "Throw it out the window",
                "time_created": get_time_created(m_id_1),
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


def test_message_send_too_long(user_a):
    """
    Test 3 - InputError - Message is > 1000 characters
    Assumes user is authorised and can join the channel
    """
    # User_a creates a channel and automatically joins
    channel_1 = channels_create(user_a["token"], "billionaire records", True)
    c_id_1 = channel_1["channel_id"]

    # Message is invalid because it is greater than 1000 characters
    with pytest.raises(InputError, match=r"Messages should be between 0 and 1000 characters long"):
        message_send(user_a["token"], c_id_1, "a" * 1001)

    clear()


def test_message_send_too_short(user_a):
    """
    Test 4 - InputError - Message is < 1 character
    Assumes user is authorised and can join the channel
    """
    # User_a creates a channel and automatically joins
    channel_1 = channels_create(user_a["token"], "billionaire records", True)
    c_id_1 = channel_1["channel_id"]

    # Message is invalid because it is less than 1 character
    with pytest.raises(InputError, match=r"Messages should be between 0 and 1000 characters long"):
        message_send(user_a["token"], c_id_1, "a" * 0)

    clear()


def test_message_send_not_in_channel(user_a, user_b):
    """
    Test 5 - AccessError - User is NOT part of the channel
    and tries to send a message
    """
    # User_a  creates a channel and automatically joins
    channel_1 = channels_create(user_a["token"], "billionaire records", True)
    c_id_1 = channel_1["channel_id"]

    # User_b does NOT join this channel and tries to send a message
    with pytest.raises(AccessError, match=r"You must be a member of the channel to view its details"):
        message_send(user_b["token"], c_id_1, "Throw it out the window")
    clear()


def test_message_send_invalid_token(user_a):
    """
    Test 6 - AccessError - Invalid Token passed in
    (refer to assumptions)
    """
    # User_a creates a channel
    channel_1 = channels_create(user_a["token"], "billionaire records", True)
    c_id_1 = channel_1["channel_id"]
    invalid_token = ""

    # AccessError should be raised since token passed is invalid
    with pytest.raises(AccessError, match=r"Invalid Token"):
        message_send(invalid_token, c_id_1, "Throw it out the window")

    clear()
