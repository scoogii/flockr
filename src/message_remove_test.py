"""
message_remove

Takes in (token, message_id)
Returns {}

Description: Given a message_id for a message, this message is removed from the channel

Exceptions:
- InputError: when message (based on ID) no longer exists
- AccessError: when NONE of the following are true
    - Message with message_id was sent by authorised user making the request
    - authorised user is an admin/owner of the channel/flockr
"""


import pytest
from auth import auth_register
from channel import channel_join, channel_messages
from channels import channels_create
from error import InputError, AccessError
from message import message_send, message_remove
from other import clear
from conftest import user_a, user_b, user_c


def test_message_remove_success_admin(user_a):
    """
    Test 1 - Test that an admin can successfully remove their own message
    """
    # User_a creates a channel and becomes owner
    channel_1 = channels_create(user_a["token"], "billionaire records", True)
    c_id_1 = channel_1["channel_id"]

    # Send the message to the channel
    msg_1 = message_send(user_a["token"], c_id_1, "Throw it out the window")
    m_id_1 = msg_1["message_id"]

    # Remove the message from the channel
    message_remove(user_a["token"], m_id_1)

    # Check that the message is no longer in the channel
    assert channel_messages(user_a["token"], c_id_1, 0) == {
        "messages": [],
        "start": 0,
        "end": -1,
    }

    clear()


def test_message_remove_success_owner(user_a, user_b):
    """
    Test 2 - Test that an owner can remove another member's message
    """
    # User_b creates a channel and becomes owner
    channel_1 = channels_create(user_b["token"], "billionaire records", True)
    c_id_1 = channel_1["channel_id"]

    # User_a joins the created channel
    channel_join(user_a["token"], c_id_1)

    # User_a sends a message to the channel
    msg_1 = message_send(user_a["token"], c_id_1, "Throw it out the window")
    m_id_1 = msg_1["message_id"]

    # User_b removes their own message
    message_remove(user_b["token"], m_id_1)

    # Check that the message is no longer in the channel
    assert channel_messages(user_b["token"], c_id_1, 0) == {
        "messages": [],
        "start": 0,
        "end": -1,
    }

    clear()


def test_message_remove_success_non_admin(user_a, user_b):
    """
    Test 3 - Test that a non-admin can successfully remove their own message
    """
    # User_a creates a channel and becomes owner
    channel_1 = channels_create(user_a["token"], "billionaire records", True)
    c_id_1 = channel_1["channel_id"]

    # User_b joins the created channel
    channel_join(user_b["token"], c_id_1)

    # User_b sends a message to the channel
    msg_1 = message_send(user_b["token"], c_id_1, "Throw it out the window")
    m_id_1 = msg_1["message_id"]

    # User_b removes their own message
    message_remove(user_b["token"], m_id_1)

    # Check that the message is no longer in the channel
    assert channel_messages(user_b["token"], c_id_1, 0) == {
        "messages": [],
        "start": 0,
        "end": -1,
    }

    clear()


def test_message_remove_success_admin_other(user_a, user_b):
    """
    Test 4 - Test that an admin can remove any other user's message
    """
    # User_a creates a channel and becomes owner
    channel_1 = channels_create(user_a["token"], "billionaire records", True)
    c_id_1 = channel_1["channel_id"]

    # User_b joins the created channel
    channel_join(user_b["token"], c_id_1)

    # User_b sends 2 message to the channel
    msg_1 = message_send(user_b["token"], c_id_1, "Throw it out the window")
    m_id_1 = msg_1["message_id"]

    msg_2 = message_send(user_b["token"], c_id_1, "I like trains")
    m_id_2 = msg_2["message_id"]

    # User_a (owner/admin) removes user_b's messages
    message_remove(user_a["token"], m_id_2)
    message_remove(user_a["token"], m_id_1)

    # Check that the message is no longer in the channel
    assert channel_messages(user_a["token"], c_id_1, 0) == {
        "messages": [],
        "start": 0,
        "end": -1,
    }

    clear()


def test_message_remove_inexistent_message(user_a):
    """
    Test 5 - InputError - Message no longer exists
    """
    # User_a creates a channel and becomes owner
    channel_1 = channels_create(user_a["token"], "billionaire records", True)
    c_id_1 = channel_1["channel_id"]

    # Send the message to the channel
    msg_1 = message_send(user_a["token"], c_id_1, "Throw it out the window")
    m_id_1 = msg_1["message_id"]

    # Remove the message from the channel
    message_remove(user_a["token"], m_id_1)

    # Try to remove a message that has already been removed
    with pytest.raises(InputError):
        message_remove(user_a["token"], m_id_1)

    clear()


def test_message_remove_invalid_permission_1(user_a, user_b):
    """
    Test 6 - AccessError - attempting to remove an admin's message without permissions
    """
    # User_a creates a channel and becomes owner
    channel_1 = channels_create(user_a["token"], "billionaire records", True)
    c_id_1 = channel_1["channel_id"]

    # User_b joins the created channel
    channel_join(user_b["token"], c_id_1)

    # User_a sends a message to the channel
    msg_1 = message_send(user_a["token"], c_id_1, "Throw it out the window")
    m_id_1 = msg_1["message_id"]

    # User_b tries to remove the message
    with pytest.raises(AccessError, match=r"You are not authorised to alter this channel"):
        message_remove(user_b["token"], m_id_1)

    clear()


def test_message_remove_invalid_permission_2(user_a, user_b, user_c):
    """
    Test 7 - AccessError - attempting to remove a user's message without permissions
    """
    # User_a creates a channel and becomes owner
    channel_1 = channels_create(user_a["token"], "billionaire records", True)
    c_id_1 = channel_1["channel_id"]

    # User_b and c join the created channel
    channel_join(user_b["token"], c_id_1)
    channel_join(user_c["token"], c_id_1)

    # User_b sends a message to the channel
    msg_1 = message_send(user_b["token"], c_id_1, "Throw it out the window")
    m_id_1 = msg_1["message_id"]

    # User_c tries to remove the message
    with pytest.raises(AccessError, match=r"You are not authorised to alter this channel"):
        message_remove(user_c["token"], m_id_1)

    clear()


def test_message_remove_invalid_permission_3(user_a, user_b, user_c):
    """
    Test 8 - AccessError - attempting to remove a user's  message without permissions
    (not the very first message)
    """
    # User_a creates a channel and becomes owner
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

    # User_c tries to remove user_b's 2nd message
    with pytest.raises(AccessError, match=r"You are not authorised to alter this channel"):
        message_remove(user_c["token"], m_id_2)

    clear()


def test_message_remove_invalid_token(user_a):
    """
    Test 9 - AccessError - Invalid token passed in
    (refer to assumptions)
    """
    # User_a creates a channel
    channel_1 = channels_create(user_a["token"], "billionaire records", True)
    c_id_1 = channel_1["channel_id"]
    invalid_token = ""

    # User_a sends a valid message to be removed
    msg_1 = message_send(user_a["token"], c_id_1, "Throw it out the window")
    m_id_1 = msg_1["message_id"]

    # AccessError should be raised since token passed is invalid
    with pytest.raises(AccessError, match=r"Invalid Token"):
        message_remove(invalid_token, m_id_1)

    clear()
