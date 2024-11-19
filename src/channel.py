"""
Channel.py
channel functions and properties
"""


from data import DATA
from auth import decode_token
from find import find_uid_from_token, find_user_from_token, find_user_from_uid
from channel_helper import (
        check_user_in_channel,
        check_u_id_in_channel,
        check_user_authorised,
        check_user_is_already_owner,
        check_user_is_owner,
        check_user_remove_owner,
        check_is_admin,
        check_remove_self,
        check_valid_channel_id,
        check_channel_priv_pub,
        check_valid_message_count,
)


########################################################################
#                          Main Functions                              #
########################################################################


def channel_invite(token, channel_id, u_id):
    """
    Invites a user to join a channel, the user is immediately added
    Parameters:
        token (str)
        channel_id (int)
        u_id (int)
    Returns:
        empty: (dict)
    """
    decoded_token = decode_token(token)

    # AccessError: token passed in is not a valid token
    find_user_from_token(decoded_token)

    # InputError: Check if the user ID is valid
    user = find_user_from_uid(u_id)

    # InputError: Check if the channel ID is valid
    channel = check_valid_channel_id(channel_id)

    # AccessError: Check if user (token) is in the channel - must be in channel
    check_user_in_channel(decoded_token, channel_id)

    # AccessError: Check if user (u_id) is already in the channel - should not be in channel
    check_u_id_in_channel(u_id, channel_id)

    new_member = {
        "u_id": u_id,
        "name_first": user["name_first"],
        "name_last": user["name_last"],
        "profile_img_url": user["profile_img_url"],
    }

    channel["all_members"].append(new_member)

    return {}


def channel_details(token, channel_id):
    """
    Returns key information about a channel the user is a part of
    Parameters:
        token (str)
        channel_id (int)
    Returns: (dict)
        name (str): the name of the channel
        owner_members (list): the owner members of the channel
        all_members (list): all members of the channel
    """
    decoded_token = decode_token(token)

    # AccessError: token passed in is not a valid token
    find_user_from_token(decoded_token)

    # InputError: Check if the channel ID is valid
    channel = check_valid_channel_id(channel_id)

    # AccessError: Check if user is in the channel
    check_user_in_channel(decoded_token, channel_id)

    return {
        "name": channel["name"],
        "owner_members": channel["owner_members"],
        "all_members": channel["all_members"],
    }


def channel_messages(token, channel_id, start):
    """
    Retrieves up to 50 messages from a channel that the user is a part of, starting
    from a given index
    Parameters:
        token (str)
        channel_id (int)
        start (int)
    Returns: (dict)
        messages (list): messages retrieved from the channel
        start (int): the requested starting index of messages to be returned
        end (int): the ending index of messages returned (-1 if least recent message is returned)
    """
    decoded_token = decode_token(token)

    # AccessError: token passed in is not a valid token
    find_user_from_token(decoded_token)

    # InputError: Check if the channel ID is valid
    check_valid_channel_id(channel_id)

    # AccessError: Check if user is in the channel
    check_user_in_channel(decoded_token, channel_id)

    # InputError: Check if start > total number of messages in channel
    check_valid_message_count(channel_id, start)

    messages = []
    # Get message_id's of messages in the channel
    c_message_ids = DATA["channels"][channel_id - 1]["messages"]

    # Go through DATA's messages and match message_id
    message_counter = 0
    for message in DATA["message_log"]["messages"]:
        if message_counter in (50, len(c_message_ids) - start):
            break
        for m_id in c_message_ids:
            if message["message_id"] == m_id:
                messages.insert(0, message)
                message_counter += 1

    # end = -1 when all least recent message has been returned
    if not c_message_ids:
        # There are no messages in the channel
        end = -1
    elif c_message_ids[-1] == messages[0]["message_id"]:
        # Least recent message has been returned
        end = -1
    else:
        # There are more messages to return
        end = start + 50

    # For each message being returned, check whether or not the user calling
    # channel_messages has reacted to them
    u_id = find_uid_from_token(decoded_token)
    for message in messages:
        if u_id in message["reacts"][0]["u_ids"]:
            message["reacts"][0]["is_this_user_reacted"] = True
        else:
            message["reacts"][0]["is_this_user_reacted"] = False

    return {
        "messages": messages,
        "start": start,
        "end": end,
    }


def channel_leave(token, channel_id):
    """
    Remove a user as a member from the channel
    Parameters:
        token (str)
        channel_id (int)
    Returns:
        empty (dict)
    """
    decoded_token = decode_token(token)

    # AccessError: token passed in is not a valid token
    find_user_from_token(decoded_token)

    # InputError: Check if the channel ID is valid
    channel = check_valid_channel_id(channel_id)

    # AccessError: Check if user is in the channel
    check_user_in_channel(decoded_token, channel_id)

    # Remove the user from the channel all member list
    index = 0
    for member in channel["all_members"]:
        if member["u_id"] == find_uid_from_token(decoded_token):
            del channel["all_members"][index]
        index += 1

    # Remove the user from the channel owner list (if they were an owner)
    index = 0
    for member in channel["owner_members"]:
        if member["u_id"] == find_uid_from_token(decoded_token):
            del channel["owner_members"][index]
        index += 1

    return {}


def channel_join(token, channel_id):
    """
    Add a user as a member of the channel
    Parameters:
        token (str)
        channel_id (int)
    Returns:
        empty (dict)
    """
    decoded_token = decode_token(token)

    # AccessError: token/u_id passed in is not a valid token
    user = find_user_from_token(decoded_token)
    u_id = find_uid_from_token(decoded_token)

    # InputError: Check if the channel ID is valid
    channel = check_valid_channel_id(channel_id)

    # AccessError: Check if the channel is public or private, if it is private
    # the user can only join if they are authorised
    if not check_channel_priv_pub(channel_id):
        check_user_authorised(u_id, channel_id)

    new_member = {
        "u_id": u_id,
        "name_first": user["name_first"],
        "name_last": user["name_last"],
        "profile_img_url": user["profile_img_url"],
    }

    channel["all_members"].append(new_member)

    return {}


def channel_addowner(token, channel_id, u_id):
    """
    Make a user an owner member of the specified channel
    Parameters:
        token (str)
        channel_id (int)
        u_id (int)
    Returns:
        empty (dict)
    """
    decoded_token = decode_token(token)

    # AccessError: token passed in is not a valid token
    find_user_from_token(decoded_token)

    # InputError: Check if the channel ID is valid
    channel = check_valid_channel_id(channel_id)

    # InputError: Check if user being made owner is already an owner
    check_user_is_already_owner(u_id, channel_id)

    # AccessError: Check if user executing command is an owner of the channel
    # First check if they are an admin since they have channel owner rights
    if not check_is_admin(find_uid_from_token(decoded_token)):
        check_user_is_owner(find_uid_from_token(decoded_token), channel_id)

    user = find_user_from_uid(u_id)

    new_owner_member = {
        "u_id": u_id,
        "name_first": user["name_first"],
        "name_last": user["name_last"],
        "profile_img_url": user["profile_img_url"],
    }

    channel["owner_members"].append(new_owner_member)

    return {}


def channel_removeowner(token, channel_id, u_id):
    """
    Remove a user as an owner member of the specified channel
    Parameters:
        token (str)
        channel_id (int)
        u_id (int)
    Returns:
        empty (dict)
    """
    decoded_token = decode_token(token)

    # AccessError: token passed in is not a valid token
    find_user_from_token(decoded_token)

    # InputError: Check if the channel ID is valid
    channel = check_valid_channel_id(channel_id)

    # AccessError: Check if user executing command is an owner of the channel
    # First check if they are an admin since they have channel owner rights
    if not check_is_admin(find_uid_from_token(decoded_token)):
        check_user_is_owner(find_uid_from_token(decoded_token), channel_id)

    # InputError: Check if the user being removed is an owner of the channel to begin with
    check_user_remove_owner(u_id, channel_id)

    for member in channel["owner_members"]:
        if member["u_id"] == u_id:
            channel["owner_members"].remove(member)

    return {}


def channel_removemember(token, channel_id, u_id):
    """
    Remove a user from the specified channel
    Parameters:
        token (str)
        channel_id (int)
        u_id (int)
    Returns:
        empty (dict)
    """
    decoded_token = decode_token(token)

    # AccessError: Check for invalid token and/or u_id
    find_user_from_token(decoded_token)
    find_user_from_uid(u_id)

    # InputError: Check if the channel ID is valid
    channel = check_valid_channel_id(channel_id)

    # AccessError: Check if user executing command is an owner of the channel
    # First check if they are an admin since they have channel owner rights
    if not check_is_admin(find_uid_from_token(decoded_token)):
        check_user_is_owner(find_uid_from_token(decoded_token), channel_id)

    # InputError: Check if user is attempting to remove themselves
    check_remove_self(decoded_token, u_id)

    # Completely remove user from channel
    for member in channel["owner_members"]:
        if member["u_id"] == u_id:
            channel["owner_members"].remove(member)

    for member in channel["all_members"]:
        if member["u_id"] == u_id:
            channel["all_members"].remove(member)

    return {}
