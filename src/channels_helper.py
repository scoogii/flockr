"""
channel_helper.py
helper functions for channel.py are sourced here
"""

from data import DATA
from error import InputError

def check_name_length(name):
    """
    Ensures that the name length of the channel is valid
    Parameters:
        name (str)
    Returns:
        None, but raises InputError if name is not valid
    """
    if len(name) > 20:
        raise InputError(description="Channel name too long")


def make_channel(name, is_public):
    """
    Makes a channel
    Parameters:
        name (str)
        is_public (bool)
    Returns:
        new_channel (dictionary): with all the details of the new channel
    """
    if not DATA["channels"]:
        c_id = 1
    else:
        c_id = len(DATA["channels"]) + 1

    new_channel = {
        "all_members": [],
        "channel_id": c_id,
        "is_public": is_public,
        "messages": [],
        "name": name,
        "owner_members": [],
    }

    return new_channel


def check_user_in_channel(u_id, channel):
    """
    Checks whether the user's u_id is part of the channel
    Parameters:
        u_id (int): the logged in user's u_id
        channel (dictionary): a channel in flockr
    Returns:
        (bool): True if user is part of channel, otherwise false
    """
    for member in channel["all_members"]:
        if member["u_id"] == u_id:
            return True

    return False
