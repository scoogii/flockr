"""
channel_messages

Takes in (token, channel_id, start)
Returns { messages, start, end }

Description:Given a Channel with ID channel_id that the authorised user is part
of, return up to 50 messages between index "start" and "start + 50".
Message with index 0 is the most recent message in the channel.
This function returns a new index "end" which is the value of "start + 50",
or, if this function has returned the least recent messages in the channel,
returns -1 in "end" to indicate there are no more messages to load after this return.

Exceptions:
- InputError when any of:
    - Channel ID is not a valid channel start is greater than the total number
    of messages in the channel
- AccessError whenAuthorised user is not a member of channel with chanel_id
"""


import pytest
from auth import auth_register
from channel import channel_join, channel_messages
from channels import channels_create
from data import DATA
from message import message_send
from error import InputError, AccessError
from other import clear, search
from conftest import user_a, user_b


def get_time_created(m_id):
    """
    Retrieves the time_created for a message given a message_id
    """
    for message in DATA["message_log"]["messages"]:
        if m_id == message["message_id"]:
            return message["time_created"]


def test_channel_message_success(user_a):
    """
    Test 1 - Testing that messages are successfully sent by the user
    """
    # User_a makes a channel
    channel_1 = channels_create(user_a["token"], "billionaire records", True)
    c_id_1 = channel_1["channel_id"]

    # Message is sent
    msg_1 = message_send(user_a["token"], c_id_1, "Throw it out the window")
    m_id_1 = msg_1["message_id"]

    # Use search function to find the time_created for the message sent
    messages = search(user_a["token"], "Throw it out the window")
    time_sent = messages["messages"][0]["time_created"]

    # Check that the message is in the channel
    assert channel_messages(user_a["token"], c_id_1, 0) == {
        "messages": [
            {
                "message_id": m_id_1,
                "u_id": user_a["u_id"],
                "message": "Throw it out the window",
                "time_created": time_sent,
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


def test_channel_message_success_50(user_a):
    """
    Test 2 - Testing that messages are retrieved correctly for over 50 messages
    """
    # User_a makes a channel
    channel_1 = channels_create(user_a["token"], "billionaire records", True)
    c_id_1 = channel_1["channel_id"]

    # Send over 50 messages (51 messages)
    message_list = []
    for i in range(0, 51):
        msg = message_send(user_a["token"], c_id_1, str(i))
        m_id = msg["message_id"]
        message_dict = {
            "message_id": m_id,
            "u_id": user_a["u_id"],
            "message": str(i),
            "time_created": get_time_created(m_id),
            "reacts": [
                {
                    "react_id": 1,
                    "u_ids": [],
                    "is_this_user_reacted": False,
                }
            ],
            "is_pinned": False,
        }
        message_list.insert(0, message_dict)

    # Remove the last message from the list because channel_messages only returns
    # 50 messages from the channel
    message_list.pop(0)
    # Check that the message is in the channel
    assert channel_messages(user_a["token"], c_id_1, 0) == {
        "messages": message_list,
        "start": 0,
        "end": 50,
    }

    clear()


def test_channel_message_invalid_channel(user_a, user_b):
    """
    Test 3 - InputError - for invalid channel ID
    """
    invalid_c_id = 4566343
    # User_a cannot check message because id is invalid
    with pytest.raises(InputError):
        # User_a makes a channel
        channel_1 = channels_create(user_a["token"], "billionaire records", True)
        c_id_1 = channel_1["channel_id"]

        # User_b joins the channel
        channel_join(user_b["token"], c_id_1)

        channel_messages(user_a["token"], invalid_c_id, 0)

    clear()


def test_channel_message_unauth_channel(user_a, user_b):
    """
    Test 4 - AccessError - for when user is not part of the channel
    """
    # User_a makes a channel
    channel_1 = channels_create(user_a["token"], "billionaire records", True)
    c_id_1 = channel_1["channel_id"]

    # User_b cannot check message because uid is invalid
    with pytest.raises(AccessError, match=r"You must be a member of the channel to view its details"):
        channel_messages(user_b["token"], c_id_1, 0)

    clear()


def test_channel_message_greater_channel(user_a, user_b):
    """
    Test 5 - InputError - for when message selections do not exist
    """
    # User_a user makes a channel
    channel_1 = channels_create(user_a["token"], "billionaire records", True)
    c_id_1 = channel_1["channel_id"]

    # User_b joins the channel
    channel_join(user_b["token"], c_id_1)

    # User_b cannot check message because start exceeds the limit of end
    with pytest.raises(InputError, match=r"Messages do not exist"):
        channel_messages(user_b["token"], c_id_1, 60)

    clear()
