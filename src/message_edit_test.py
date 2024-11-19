"""
message_edit

Takes in parameters `token`, `message_id`, `message`
Returns an empty dictionary {}

Description: Given a message, update it's text with new text.
If the new message is an empty string, the message is deleted.

Exceptions:
 - AccessError: User is trying to edit a message that is
   not theirs OR they do not have admin privileges
"""


import pytest
from auth import auth_register
from channel import channel_join, channel_messages
from channels import channels_create
from data import DATA
from error import AccessError, InputError
from message import message_send, message_edit
from other import clear
from conftest import user_a, user_b, user_c


def get_time_created(m_id):
    """
    Retrieves the time_created for a message given a message_id
    """
    for message in DATA["message_log"]["messages"]:
        if m_id == message["message_id"]:
            return message["time_created"]


def test_message_edit_success_own_message(user_a):
    """
    Test 1 - user succesfully edits their own message
    """
    # User_a creates a channel and become owner
    channel_1 = channels_create(user_a["token"], "billionaire records", True)
    c_id_1 = channel_1["channel_id"]

    # Send the message to the channel
    msg_1 = message_send(user_a["token"], c_id_1, "Throw it out the window")
    m_id_1 = msg_1["message_id"]

    # Edit the message in the channel
    message_edit(user_a["token"], m_id_1, "I like trains")

    # Check that the message has been edited
    assert channel_messages(user_a["token"], c_id_1, 0) == {
        "messages": [
            {
                "message_id": m_id_1,
                "u_id": user_a["u_id"],
                "message": "I like trains",
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


def test_message_edit_success_owner(user_b, user_c):
    """
    Test 2 - Owner of channel succesfully edits someone
    else's message
    """
    # User_b creates a channel and becomes owner
    channel_1 = channels_create(user_b["token"], "billionaire records", True)
    c_id_1 = channel_1["channel_id"]

    # User_c joins the created channel
    channel_join(user_c["token"], c_id_1)

    # User_c sends a message to the channel
    msg_1 = message_send(user_c["token"], c_id_1, "Throw it out the window")
    m_id_1 = msg_1["message_id"]

    # User_b owner edits the message in the channel
    message_edit(user_b["token"], m_id_1, "I like trains")

    # Check that the message has been edited
    assert channel_messages(user_b["token"], c_id_1, 0) == {
        "messages": [
            {
                "message_id": m_id_1,
                "u_id": user_c["u_id"],
                "message": "I like trains",
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


def test_message_edit_success_admin(user_a, user_b):
    """
    Test 3 - Admin/owner succesfully edits someone
    else's message
    """
    # User_a creates a channel and becomes owner
    channel_1 = channels_create(user_a["token"], "billionaire records", True)
    c_id_1 = channel_1["channel_id"]

    # User_b joins the created channel
    channel_join(user_b["token"], c_id_1)

    # User_b sends 2 messages to the channel
    msg_1 = message_send(user_b["token"], c_id_1, "Throw it out the window")
    m_id_1 = msg_1["message_id"]

    msg_2 = message_send(user_b["token"], c_id_1, "I like trains")
    m_id_2 = msg_2["message_id"]

    # User_a (admin/owner) edits the 2nd message in the channel
    message_edit(user_a["token"], m_id_2, "My name Jeff")

    # Check that the message has been edited
    assert channel_messages(user_a["token"], c_id_1, 0) == {
        "messages": [
            {
                "message_id": m_id_2,
                "u_id": user_b["u_id"],
                "message": "My name Jeff",
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
                "u_id": user_b["u_id"],
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


def test_message_edit_success_empty(user_a):
    """
    Test 4 - User updates message with empty string
    (message is deleted)
    """
    # User creates a channel and become owner
    channel_1 = channels_create(user_a["token"], "billionaire records", True)
    c_id_1 = channel_1["channel_id"]

    # Send the message to the channel
    msg_1 = message_send(user_a["token"], c_id_1, "Throw it out the window")
    m_id_1 = msg_1["message_id"]

    # Edit the message in the channel with empty string
    message_edit(user_a["token"], m_id_1, "")

    # Check that the message has been deleted
    assert channel_messages(user_a["token"], c_id_1, 0) == {
        "messages": [],
        "start": 0,
        "end": -1,
    }

    clear()


def test_message_edit_invalid_premission_1(user_a, user_b):
    """
    Test 5 - AccessError - User tries to edit someone
    else's message but is not an admin/owner while the
    other person is an owner
    """
    # User_a creates a channel and become owner
    channel_1 = channels_create(user_a["token"], "billionaire records", True)
    c_id_1 = channel_1["channel_id"]

    # User_b joins the created channel
    channel_join(user_b["token"], c_id_1)

    # User_a sends a message to the channel
    msg_1 = message_send(user_a["token"], c_id_1, "Throw it out the window")
    m_id_1 = msg_1["message_id"]

    # User_b tries edits the message in the channel
    with pytest.raises(AccessError, match=r"You are not authorised to alter this channel"):
        message_edit(user_b["token"], m_id_1, "I like trains")

    clear()


def test_message_edit_invalid_premission_2(user_a, user_b, user_c):
    """
    Test 6 - AccessError - User tries to edit someone
    else's message but is not an admin/owner while the
    other person also isn't
    """
    # User_a creates a channel and become owner
    channel_1 = channels_create(user_a["token"], "billionaire records", True)
    c_id_1 = channel_1["channel_id"]

    # User_b and c join the created channel
    channel_join(user_b["token"], c_id_1)
    channel_join(user_c["token"], c_id_1)

    # User_b sends a message to the channel
    msg_1 = message_send(user_b["token"], c_id_1, "Throw it out the window")
    m_id_1 = msg_1["message_id"]

    # User_c tries edits the message in the channel
    with pytest.raises(AccessError, match=r"You are not authorised to alter this channel"):
        message_edit(user_c["token"], m_id_1, "I like trains")

    clear()


def test_message_edit_invalid_premission_3(user_a, user_b, user_c):
    """
    Test 7 - AccessError - User tries to edit someone
    else's message but is not an admin/owner while the
    other person also isn't (not first message)
    """
    # User_a creates a channel and become owner
    channel_1 = channels_create(user_a["token"], "billionaire records", True)
    c_id_1 = channel_1["channel_id"]

    # User_b and c join the created channel
    channel_join(user_b["token"], c_id_1)
    channel_join(user_c["token"], c_id_1)

    # User_b sends 3 messages to the channel
    message_send(user_b["token"], c_id_1, "Throw it out the window")

    msg_2 = message_send(user_b["token"], c_id_1, "I like trains")
    m_id_2 = msg_2["message_id"]

    message_send(user_b["token"], c_id_1, "My name Jeff")

    # User_c tries edits the 2nd message in the channel
    with pytest.raises(AccessError, match=r"You are not authorised to alter this channel"):
        message_edit(user_c["token"], m_id_2, "My name Jeff")

    clear()


def test_message_edit_invalid_token(user_a):
    """
    Test 8 - AccessError - Invalid token passed in
    (refer to assumptions)
    """
    # User_a creates a channel
    channel_1 = channels_create(user_a["token"], "billionaire records", True)
    c_id_1 = channel_1["channel_id"]
    invalid_token = ""

    # User_a sends a valid message to be edited
    msg_1 = message_send(user_a["token"], c_id_1, "Throw it out the window")
    m_id_1 = msg_1["message_id"]

    # AccessError should be raised since token passed is invalid
    with pytest.raises(AccessError, match=r"Invalid Token"):
        message_edit(invalid_token, m_id_1, "This isn't getting edited")

    clear()


def test_message_edit_too_long(user_a):
    """
    Test 9 - InputError - User tries to edit a message
    that is > 1000 characters
    """
    # User creates a channel and become owner
    channel_1 = channels_create(user_a["token"], "billionaire records", True)
    c_id_1 = channel_1["channel_id"]

    # Edited message is invalid because it is less than 1 character
    with pytest.raises(InputError, match=r"Messages should be between 0 and 1000 characters long"):
        message_edit(user_a["token"], c_id_1, "a" * 1001)

    clear()
