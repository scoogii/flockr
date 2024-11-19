"""
message_helper.py
helper functions for message.py are sourced from here
"""


from data import DATA
from datetime import datetime
from error import InputError, AccessError
from find import find_uid_from_token, find_cid_from_mid


def check_already_pinned(message_id):
    """
    Checks whether a message is already pinned
    Parameters:
        message_id (int)
    Returns:
        (void): Raises an InputError if the user is attempting
                to pin a message that is already pinned
    """
    pinned = False
    for messages in DATA["message_log"]["messages"]:
        if messages["message_id"] == message_id and messages["is_pinned"]:
            pinned = True

    if pinned:
        raise InputError(description="Message is already pinned")


def check_already_reacted(token, message_id, react_id):
    """
    Checks if a user has already reacted to a message with a given
    react_id
    Parameters:
        token (str)
        message_id (int)
        react_id (int)
    Returns:
        (void): Raises an InputError if the user has
                already reacted to the message with a given react_id
    """
    u_id = find_uid_from_token(token)
    react_uids = []
    for messages in DATA["message_log"]["messages"]:
        if message_id == messages["message_id"]:
            react_uids = messages["reacts"][0]["u_ids"]

    if u_id in react_uids:
        raise InputError(f"Message already has react {react_id}")


def check_already_unpinned(message_id):
    """
    Checks whether a message is already unpinned
    Parameters:
        message_id (int)
    Returns:
        (void): Raises an InputError if the user is attempting
                to unpin a message that is already unpinned
    """
    pinned = False
    for messages in DATA["message_log"]["messages"]:
        if messages["message_id"] == message_id and messages["is_pinned"]:
            pinned = True

    if not pinned:
        raise InputError(description="Message is already unpinned")


def check_already_unreacted(token, message_id, react_id):
    """
    Checks if a user has already unreacted to a message with a given
    react_id
    Parameters:
        token (str)
        message_id (int)
        react_id (int)
    Returns:
        (void): Raises an InputError if the user has
                already unreacted to the message with a given react_id
    """
    u_id = find_uid_from_token(token)
    react_uids = []
    for messages in DATA["message_log"]["messages"]:
        if message_id == messages["message_id"]:
            react_uids = messages["reacts"][0]["u_ids"]

    if u_id not in react_uids:
        raise InputError(f"Message does not have react {react_id}")


def check_message_length_send(message):
    """
    Checks whether the message is a valid length
    Parameters:
        message (str)
    Returns:
        None, but raises InputError if message length is invalid
    """
    if len(message) not in range(1, 1001):
        raise InputError("Messages should be between 0 and 1000 characters long")


def check_message_length_edit(message):
    """
    Checks whether the message is a valid length
    Parameters:
        message (str)
    Returns:
        None, but raises InputError if message length is invalid
    """
    if len(message) not in range(1001):
        raise InputError("Messages should be between 0 and 1000 characters long")


def check_message_exists(m_id):
    """
    Checks whether the message to be modified exists
    Parameters:
        m_id (int)
    Returns:
        True if corresponding message exists, otherwise False
    """
    for message in DATA["message_log"]["messages"]:
        if message["message_id"] == m_id:
            return True

    raise InputError(f"Message: {m_id} does not exist")


def check_react_id(react_id):
    """
    Checks if a given react_id is valid
    Parameters:
        react_id (int)
    Returns:
        (bool): returns "True" if the react_id is valid, otherwise
            it will raise an InputError
    """
    if react_id == 1:
        return True

    raise InputError(f"React {react_id} does not exist")


def check_time_sent_past(time_sent):
    """
    Checks whether the time for the message to be sent later
    is not before the current time
    Parameters:
        time_sent (int)
    Returns:
        (void): Raises an InputError if the time requested to be sent
        is before the current time
    """
    if time_sent < int((datetime.now().timestamp())):
        raise InputError(description="Left bound is greater than the right bound")


def check_self_modify(token, m_id):
    """Check that the message to be modified will be done by
       the user who sent it
    Parameters:
        token (str)
        m_id (int)
    Returns:
        (bool): True if the above condition is satisfied, otherwise False
    """
    for message in DATA["message_log"]["messages"]:
        if message["message_id"] == m_id:
            if message["u_id"] == find_uid_from_token(token):
                return True

    return False


def check_owner_modify(token, m_id):
    """Check that the message to be modified will be done by
       an owner of the channel or an owner
    Parameters:
        token (str)
    Returns:
        (bool): True if the above condition is satisfied, otherwise False
    """
    c_id = find_cid_from_mid(m_id)
    u_id = find_uid_from_token(token)

    for owner in DATA["channels"][c_id - 1]["owner_members"]:
        if owner["u_id"] == u_id:
            return True

    raise AccessError(description="You are not authorised to alter this channel")
