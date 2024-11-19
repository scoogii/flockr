"""
Channels.py
creating and listing channels
"""


from channel import channel_join
from data import DATA
from auth import decode_token
from find import find_uid_from_token, find_user_from_token
from channels_helper import (
    check_name_length,
    make_channel,
    check_user_in_channel,
)


########################################################################
#                            Main Functions                            #
########################################################################


def channels_create(token, name, is_public):
    """
    Creates a new channel with a given name and is set to either a public
       or private channel
    Parameters:
        token (str)
        name (str)
        is_public (bool)
    Returns:
        {"channel_id": c_id}: a dictionary pair containing the channel_id
        of the created channel
    """
    decoded_token = decode_token(token)

    # AccessError: token passed in is not a valid token
    find_user_from_token(decoded_token)

    # Test for invalid name length - raise exception if invalid
    check_name_length(name)

    # Make a new channel dict and add it to the DATA for channels
    new_channel = make_channel(name, is_public)
    DATA["channels"].append(new_channel)
    c_id = new_channel["channel_id"]

    # Once channel is made, user should become owner of channel then join
    owner = find_user_from_token(decoded_token)
    DATA["channels"][c_id - 1]["owner_members"].append(
        {
            "u_id": owner["u_id"],
            "name_first": owner["name_first"],
            "name_last": owner["name_last"],
            "profile_img_url": owner["profile_img_url"],
        }
    )
    channel_join(token, c_id)

    return {"channel_id": c_id}


def channels_list(token):
    """
    Provides a list of all channels (and their associated details) that
       the authorised user is part of
    Parameters:
        token (str)
    Returns:
        channels_in (dictionary): contains a list of dictionaries
        of all the channels the user is part of
    """
    decoded_token = decode_token(token)

    # AccessError: token passed in is not a valid token
    find_user_from_token(decoded_token)

    # Create a dictionary that will contain all channels user is in
    channels_in = {"channels": []}

    # Loop through channels, if user part of channel add details to channels_in
    for channel in DATA["channels"]:
        if check_user_in_channel(find_uid_from_token(decoded_token), channel):
            channels_in["channels"].append(
                {"channel_id": channel["channel_id"], "name": channel["name"]}
            )

    return channels_in


# Provide a list of ALL channels (and their associated details)
# Returns a dictionary with a list of all channels
def channels_listall(token):
    """
    Provides a list of ALL channels (and their associated details)
    Parameters:
        token (str)
    Returns:
        channels_all (dictionary): contains a list of dictionaries
        of all the channels in flockr
    """
    decoded_token = decode_token(token)

    # Check for invalid token before showing all channels
    find_user_from_token(decoded_token)

    # Create a dictionary that will contain all channels
    channels_all = {"channels": []}

    # Loop through all channels and add details to channels_all
    for channel in DATA["channels"]:
        channels_all["channels"].append(
            {"channel_id": channel["channel_id"], "name": channel["name"]}
        )

    return channels_all
