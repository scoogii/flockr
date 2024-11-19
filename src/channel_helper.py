"""
channel_helper.py
helper functions for channel.py are sourced here
"""


from data import DATA
from error import AccessError, InputError
from find import find_uid_from_token


def check_user_in_channel(token, channel_id):
    """
    Checks if a user is in a specified channel
    Parameters:
        token (str)
        channel_id (int)
    Returns:
        (bool): "True" if the user is inside the channel or AccessError
                if the user is not
    """
    for member in DATA["channels"][channel_id - 1]["all_members"]:
        if member["u_id"] == find_uid_from_token(token):
            return True

    raise AccessError(description="You must be a member of the channel to view its details")


def check_u_id_in_channel(u_id, channel_id):
    """
    Checks if a user with u_id is in a specified channel
    Parameters:
        u_id (int)
        channel_id (int)
    Returns:
        (bool): InputError if the user is already inside the channel or "True"
                if the user is not
    """
    for member in DATA["channels"][channel_id - 1]["all_members"]:
        if member["u_id"] == u_id:
            raise InputError(description="User already a member of this channel")

    return True


def check_user_authorised(u_id, channel_id):
    """
    Checks if a user is authorised to join the channel
    Parameters:
        u_id (int)
        channel_id (int)
    Returns:
        (bool): "True" if the user is authorised to join the channel
                and AccessError if the user is not
    """
    for user in DATA["users"]:
        if user["u_id"] == u_id and user["permission_id"] == 1:
            return True

    for member in DATA["channels"][channel_id - 1]["owner_members"]:
        if member["u_id"] == u_id:
            return True

    raise AccessError(description="User is not authorised to join channel")


def check_user_is_already_owner(u_id, channel_id):
    """
    Checks if a user is already an owner of a channel when being added
    as an owner
    Parameters:
        u_id (int)
        channel_id (int)
    Returns:
        (void): raises InputError if the user is already an owner of
                the channel
    """
    for member in DATA["channels"][channel_id - 1]["owner_members"]:
        if member["u_id"] == u_id:
            raise InputError(description="User is already an owner")


def check_user_is_owner(u_id, channel_id):
    """
    Checks if a user is an owner of a channel when attempting to
    access certain permissions
    Parameters:
        u_id (int)
        channel_id (int)
    Returns:
        (bool): returns "True" if the user is an owner or raises
                AccessError if the user is not
    """
    for member in DATA["channels"][channel_id - 1]["owner_members"]:
        if member["u_id"] == u_id:
            return True

    raise AccessError(description="User is not an owner")


def check_user_remove_owner(u_id, channel_id):
    """
    Checks if a user is not an owner of a channel when attempted to be
    removed as an owner
    Parameters:
        u_id (int)
        channel_id (int)
    Returns:
        (bool): returns "True" if the user is an owner or raises
                AccessError if the user is not
    """
    for member in DATA["channels"][channel_id - 1]["owner_members"]:
        if member["u_id"] == u_id:
            return True

    raise InputError(description="User being removed as owner is not an owner")


def check_is_admin(u_id):
    """
    Using the user's u_id, checks if the user is an admin of Flockr
    If so, they should automatically become a channel owner when joining
    regardless of whether the channel is pub/priv. Admin also cannot be
    removed as a channel owner
    Parameters:
        u_id (int)
        channel_id (int)
    Returns:
        (bool): returns "True" if the user is a Flockr admin
                returns "False" if user is not and the user is joining
                raises an AccessError if not and the user is being removed
                as an owner
    """
    for user in DATA["users"]:
        if user["u_id"] == u_id and user["permission_id"] == 1:
            return True

    return False


def check_remove_self(token, u_id):
    if find_uid_from_token(token) == u_id:
        raise InputError(description="Removing yourself from the channel is not allowed")


# ____________________________Channel Functions_________________________#


def check_valid_channel_id(channel_id):
    """
    Checks if the channel ID is valid
    Parameters:
        channel_id (int)
    Returns:
        (bool): "True" if the channel ID exists or InputError
                if it does not
    """

    for channel in DATA["channels"]:
        if channel["channel_id"] == channel_id:
            return channel

    raise InputError(description=f"Channel: {channel_id} does not exist")


# Check if a channel is private or public
# Go into DATA to check for is_public boolean (True or False)
def check_channel_priv_pub(channel_id):
    """
    Checks if the channel is public or private
    Parameters:
        channel_id (int)
    Returns:
        (bool): "True" if the channel is public or "False"
                if it is private
    """
    return DATA["channels"][channel_id - 1]["is_public"]


# ____________________________Message Functions_________________________#


def check_valid_message_count(channel_id, start):
    """
    Checks if the requested start index of messages in a channel is valid
    Parameters:
        channel_id (int)
        start (int): the requested starting index of messages to be returned
    Returns:
        (void): raises InputError if the starting index exceeds the number
                of messages in the channel
    """
    if start > len(DATA["channels"][channel_id - 1]["messages"]):
        raise InputError(description="Messages do not exist")
