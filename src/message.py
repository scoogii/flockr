"""
Message.py
Sending, removing and editing messages
"""


from datetime import datetime
from threading import Timer
from auth import decode_token
from data import DATA
from error import AccessError, InputError
from find import find_uid_from_token, find_cid_from_mid
from channel_helper import (
    check_valid_channel_id,
    check_user_in_channel,
    check_is_admin,
)
from message_helper import (
    check_already_pinned,
    check_already_reacted,
    check_already_unpinned,
    check_already_unreacted,
    check_message_length_send,
    check_message_length_edit,
    check_message_exists,
    check_react_id,
    check_time_sent_past,
    check_self_modify,
    check_owner_modify,
)


########################################################################
#                          Main Functions                              #
########################################################################

def send_message(u_id, channel_id, message, m_id):
    """
    Sends a message from a user with given u_id
    Parameters:
        u_id (int)
        channel_id (int)
        message (str)
        m_id (int) - defaulted to None
    Returns:
        None
    """
    # Make a new message dict to be added to the channel's messages
    new_message = {
        "message_id": m_id,
        "u_id": u_id,
        "message": message,
        "time_created": int((datetime.now()).timestamp()),
        "reacts": [
            {
                "react_id": 1,
                "u_ids": [],
                "is_this_user_reacted": False,
            }
        ],
        "is_pinned": False,
    }

    # Add message details to the DATA's messages, and
    # message_id to the current channel and to the user's sent messages
    DATA["message_log"]["messages"].append(new_message)
    DATA["channels"][channel_id - 1]["messages"].append(m_id)
    DATA["users"][u_id - 1]["user_message_id"].append(m_id)

    return


def message_send(token, channel_id, message):
    """
    Sends a message to the specified channel
    Parameters:
        token (str)
        channel_id (int)
        message (str)
    Returns:
        message_id (int)
    """
    decoded_token = decode_token(token)

    # Check the length of the message is valid
    check_message_length_send(message)

    # Check that the current user is in the channel
    u_id = find_uid_from_token(decoded_token)
    check_user_in_channel(decoded_token, channel_id)

    m_id = DATA["message_log"]["msg_counter"]
    DATA["message_log"]["msg_counter"] += 1

    send_message(u_id, channel_id, message, m_id)

    return {"message_id": m_id}


def message_remove(token, message_id):
    """
    Removes a message from the specified channel
    Parameters:
        token (str)
        message_id (int)
    Returns:
        empty (dict)
    """
    decoded_token = decode_token(token)

    # Check that the message to be deleted exists
    check_message_exists(message_id)

    # Check that the user is removing their own message
    # unless they are an owner of the channel or Flockr
    if not check_self_modify(decoded_token, message_id):
        if not check_is_admin(find_uid_from_token(decoded_token)):
            check_owner_modify(decoded_token, message_id)

    # Remove the message_id from the channel's messages
    for channel in DATA["channels"]:
        for m_id in channel["messages"]:
            if m_id == message_id:
                channel["messages"].remove(m_id)

    # Remove messages from messages DATA
    DATA["message_log"]["messages"] = [
        msg for msg in DATA["message_log"]["messages"]
        if not (msg["message_id"] == message_id)
    ]

    # Remove message from user's sent messages
    u_id = find_uid_from_token(decoded_token)
    DATA["users"][u_id - 1]["user_message_id"] = [
        m_id for m_id in DATA["users"][u_id - 1]["user_message_id"]
        if not (m_id == message_id)
    ]

    return {}


def message_edit(token, message_id, message):
    """
    Edits a given message
    Parameters:
        token (str)
        message_id (int)
        message (str)
    Returns:
        empty (dict)
    """
    # Check message length is less than 1001 characters
    check_message_length_edit(message)

    # Check if the edited message empty - remove in that case
    if not message:
        message_remove(token, message_id)
        return {}

    decoded_token = decode_token(token)

    # Check that the user is editing their own message
    # unless they are an owner of the channel or Flockr
    if not check_self_modify(decoded_token, message_id):
        if not check_is_admin(find_uid_from_token(decoded_token)):
            check_owner_modify(decoded_token, message_id)

    # Edit the message from the DATA's message log
    for messages in DATA["message_log"]["messages"]:
        if messages["message_id"] == message_id:
            messages["message"] = message

    return {}


def message_react(token, message_id, react_id):
    """
    Reacts to a given message
    Parameters:
        token (str)
        message_id (int)
        react_id (int)
    Returns:
        empty (dict)
    """
    decoded_token = decode_token(token)

    # Check if the message_id is valid
    check_message_exists(message_id)

    # Check that the react_id is valid
    check_react_id(react_id)

    # Check if the user already reacted to the message with the same react_id
    check_already_reacted(decoded_token, message_id, react_id)

    for messages in DATA["message_log"]["messages"]:
        if messages["message_id"] == message_id:
            messages["reacts"][0]["u_ids"].append(find_uid_from_token(decoded_token))
            messages["reacts"][0]["is_this_user_reacted"] = True

    return {}


def message_unreact(token, message_id, react_id):
    """
    Unreacts to a given message
    Parameters:
        token (str)
        message_id (int)
        react_id (int)
    Returns:
        empty (dict)
    """
    decoded_token = decode_token(token)

    # Check if the message_id is valid
    check_message_exists(message_id)

    # Check that the react_id is valid
    check_react_id(react_id)

    # Check if the user already unreacted to the message with the same react_id
    check_already_unreacted(decoded_token, message_id, react_id)

    for messages in DATA["message_log"]["messages"]:
        if messages["message_id"] == message_id:
            messages["reacts"][0]["u_ids"].remove(find_uid_from_token(decoded_token))
            messages["reacts"][0]["is_this_user_reacted"] = False

    return {}


def message_pin(token, message_id):
    """
    Pins a given message
    Parameters:
        token (str)
        message_id (int)
    Returns:
        empty (dict)
    """
    decoded_token = decode_token(token)

    # Check if the message_id is valid
    check_message_exists(message_id)

    # Check if the message has already been pinned
    check_already_pinned(message_id)

    # Check if user is a member of the channel
    c_id = find_cid_from_mid(message_id)

    check_user_in_channel(decoded_token, c_id)

    # Check if user is an admin of Flockr, if not - check if they're a channel owner
    if not check_is_admin(find_uid_from_token(decoded_token)):
        check_owner_modify(decoded_token, message_id)

    for messages in DATA["message_log"]["messages"]:
        if messages["message_id"] == message_id:
            messages["is_pinned"] = True

    return {}


def message_unpin(token, message_id):
    """
    Unpins a given message
    Parameters:
        token (str)
        message_id (int)
    Returns:
        empty (dict)
    """
    decoded_token = decode_token(token)

    # Check if the message_id is valid
    check_message_exists(message_id)

    # Check if the message has already been unpinned
    check_already_unpinned(message_id)

    # Check if user is a member of the channel
    c_id = find_cid_from_mid(message_id)

    check_user_in_channel(decoded_token, c_id)

    # Check if user is an admin of Flockr, if not - check if they're a channel owner
    if not check_is_admin(find_uid_from_token(decoded_token)):
        check_owner_modify(decoded_token, message_id)

    for messages in DATA["message_log"]["messages"]:
        if messages["message_id"] == message_id:
            messages["is_pinned"] = False

    return {}


def message_sendlater(token, channel_id, message, time_sent):
    """
    Sends a message from authorised user to the channel specified
    by channel_id automatically at a specified time in the future
    Parameters:
        token (str)
        channel_id (int)
        message (str)
        time_sent (int)
    Returns:
        {message_id} (dict)
    """
    decoded_token = decode_token(token)

    # Check the channel_id is valid
    check_valid_channel_id(channel_id)

    # Check message length is valid
    check_message_length_send(message)

    # Check the time_sent is not in the past
    check_time_sent_past(time_sent)

    # Check if user is a member of the channel
    u_id = find_uid_from_token(decoded_token)
    check_user_in_channel(decoded_token, channel_id)

    m_id = DATA["message_log"]["msg_counter"]
    DATA["message_log"]["msg_counter"] += 1

    # Calculate the remaining time before sending message in seconds
    remaining_time = time_sent - int((datetime.now()).timestamp())
    timer = Timer(remaining_time, send_message, [u_id, channel_id, message, m_id])
    timer.start()

    return {"message_id": m_id}
