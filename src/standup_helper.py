"""
standup_helper.py
helper functions for standup.py are sourced from here
"""

from datetime import datetime, timedelta
from auth import encode_token
from data import DATA
from error import InputError
from message import message_send


def get_finish_time(length):
    """
    Gets the time when standup finishes
    Parameters:
        length (int)
    Returns:
        time finished (int)
    """
    # Actual start time
    start = datetime.now()
    # Actual finish time
    finish = start + timedelta(seconds=length)
    return int(finish.timestamp())


def find_standup(channel_id):
    """
    Finds the standup for a given channel
    Parameters:
        channel_id (int)
    Returns:
        standup (dict)
    """
    for standup in DATA["standup"]:
        if standup["channel_id"] == channel_id:
            channel_standup = standup

    return channel_standup


def standup_running(channel_id):
    """
    Checks if a standup is running
    Parameters:
        channel_id (int)
    Returns:
        Raises InputError if the standup is already running
        Otherwise, None
    """
    for standup in DATA["standup"]:
        if standup["channel_id"] == channel_id and standup["is_active"]:
            raise InputError(description="Standup is already running")


def standup_not_running(channel_id):
    """
    Checks if a standup is not running
    Parameters:
        channel_id (int)
    Returns:
        Raises InputError if the standup isn't running
        Otherwise, None
    """
    active = False
    for standup in DATA["standup"]:
        if standup["channel_id"] == channel_id and  standup["is_active"]:
            active = True

    if not active:
        raise InputError(description="Standup is not running")


def make_standup(u_id, channel_id, length):
    """
    Function that makes a new standup for the given channel
    and adds it to the data
    Parameters:
        u_id (int)
        channel_id (int)
        length (int)
    Returns:
        None
    """
    finish_time = get_finish_time(length)

    # Make a new standup based on channel_id, u_id and the finish time
    new_standup = {
        "channel_id": channel_id,
        "messages": [],
        "sender": [],
        "is_active": True,
        "time_finish": finish_time,
        "standup_user": u_id,
    }

    DATA["standup"].append(new_standup)


def standup_append(standup):
    """
    Retrieves messages from a standup and sends them to the channel
    Parameters:
        standup (dict)
    Returns:
        None
    """
    # Standup send
    standup_msg = ""
    index = 0
    for message in standup["messages"]:
        sender = standup["sender"][index]

        standup_msg += str(sender) + ": " + message + "\n"
        index += 1

    # remove trailing newline
    standup_msg.rstrip()

    token = encode_token(standup["standup_user"])

    # Sends the message
    message_send(token, standup["channel_id"], standup_msg)


def standup_finish_switch():
    """
    Stops the standup and resets all standup information
    This function could be called from server frequently (every second while it is running)
    Once the time has passed / is finished it will call the append function to package the message
    Parameters:
        None
    Returns:
        None
    """
    now = (datetime.now()).timestamp()
    for standup in DATA["standup"]:
        if (standup["time_finish"]) and (now > standup["time_finish"]):
            # If there are messages call standup_append to package any messages and send them
            if standup["messages"]:
                standup_append(standup)
            standup["messages"] = []
            standup["sender"] = []
            standup["time_finish"] = None
            standup["standup_user"] = None
            standup["is_active"] = False


def standup_activate(u_id, channel_id, length):
    """
    Activates standup period within a channel
    If none exists, make a standup
    Parameters:
        u_id (int)
        channel_id (int)
        length (int)
    Returns:
        None
    """
    standup_found = False
    finish_time = get_finish_time(length)
    for standup in DATA["standup"]:
        if standup["channel_id"] == channel_id:
            standup_found = True
            standup["time_finish"] = finish_time
            standup["standup_user"] = u_id
            standup["is_active"] = True

    if not standup_found:
        make_standup(u_id, channel_id, length)


def standup_msg_long(message):
    """
    Checks whether a standup message is too long
    Parameters:
        message (str)
    Returns:
        Raises InputError if the message is more than 1000 characters
        Otheriwse None
    """
    if len(message) > 1000:
        raise InputError(description="Messages should be between 0 and 1000 characters long")
