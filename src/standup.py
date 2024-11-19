"""
Standup.py
standup functions and properties
"""


from threading import Timer
from data import DATA
from auth import decode_token
from find import find_uid_from_token, find_user_from_token
from channel import check_valid_channel_id, check_user_in_channel
from standup_helper import (
    find_standup,
    standup_running,
    standup_not_running,
    standup_finish_switch,
    standup_activate,
    standup_msg_long
)


########################################################################
#                          Main Functions                              #
########################################################################


def standup_active(token, channel_id):
    """
    Takes in (token, channel_id)
    Returns { is_active, time_finish }

    Description: For a given channel, return whether a standup is active in it,
    and what time the standup finishes.
    If no standup is active, then time_finish returns None

    Exceptions:
    - InputError when any of:
    - Channel ID is not a valid channel
    """
    # Error checking
    # Check if channel_id is valid
    check_valid_channel_id(channel_id)

    # Decode and check if token is valid
    decoded_token = decode_token(token)
    find_user_from_token(decoded_token)

    # Call function to set finished standups as not active
    standup_finish_switch()

    status = False
    # Search through the data to check if the channel_id is in the standup data
    for standup in DATA["standup"]:
        if standup["channel_id"] == channel_id:
            status = standup["is_active"]
            finish = standup["time_finish"]
            # Standup is found
            return {"is_active": status, "time_finish": finish}

    # No standup is found so status will be false and time finish will be none
    return {"is_active": status, "time_finish": None}


def standup_start(token, channel_id, length):
    """
    standup_start

    Takes in (token, channel_id, length)
    Returns { time_finish }

    Description: Start the standup period whereby for the next "length"/X seconds
    all calls to "standup_send" with a message, are collected during the X second window
    and added to the message queue in the channel from the user who started the standup.

    Exceptions:
    - InputError when any of:
        - Channel ID is not a valid channel
        - An active standup is currently running in this channel

    """
    # Decode the token and check if it belongs to a user
    decoded_token = decode_token(token)
    find_user_from_token(decoded_token)

    # Get u_id from the token
    u_id = find_uid_from_token(decoded_token)

    # Check if channel_id is valid
    check_valid_channel_id(channel_id)

    # Check if the standup is already running
    standup_running(channel_id)

    # Activate the standup
    standup_activate(u_id, channel_id, length)

    # Use a timer
    Timer(float(length), standup_finish_switch).start()

    standup = find_standup(channel_id)
    finish = standup["time_finish"]

    # Return the finish time
    return {"time_finish": finish}


def standup_send(token, channel_id, message):
    """
    standup_send

    Takes in (token, channel_id, length)
    Returns {}

    Description: Sending a message to get buffered in the standup queue,
    assuming a standup is currently active

    Exceptions:
    - InputError when any of:
        - Channel ID is not a valid channel
        - Message is more than 1000 characters
        - An active standup is currently running in this channel

    - AccessError when any of:
        - The authorised user is not a member of the channel that the message is within

    """
    # Check if channel_id is valid
    check_valid_channel_id(channel_id)

    # Decode the token
    decoded_token = decode_token(token)
    # Get u_id from the token
    user = find_user_from_token(decoded_token)

    # Check if the user is in the channel
    check_user_in_channel(decoded_token, channel_id)

    # Error check if the standup is not running
    standup_not_running(channel_id)

    # Error check if the message is too long
    standup_msg_long(message)

    # Add message to the list
    standup = find_standup(channel_id)
    standup["messages"].append(message)
    standup["sender"].append(user["handle_str"])

    return {}
