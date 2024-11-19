"""
http_channel_functions

HTTP functions of channel functions for testing
"""


import requests


def http_channel_addowner(url, token, channel_id, u_id):
    """
    Function that makes a HTTP request to make another user an
    owner
    Parameters:
        url
        token (str)
        channel_id (int)
        u_id (int)
    Returns:
        JSON data returned from request
    """
    channel_addowner_info = {
        "token": token,
        "channel_id": channel_id,
        "u_id": u_id,
    }

    return requests.post(f"{url}/channel/addowner", json=channel_addowner_info)


def http_channel_removeowner(url, token, channel_id, u_id):
    """
    Function that makes a HTTP request to remove another user from
    being an owner
    Parameters:
        url
        token (str)
        channel_id (int)
        u_id (int)
    Returns:
        JSON data returned from request
    """
    channel_removeowner_info = {
        "token": token,
        "channel_id": channel_id,
        "u_id": u_id,
    }

    return requests.post(f"{url}/channel/removeowner", json=channel_removeowner_info)


def http_channel_details(url, token, channel_id):
    """
    Function that makes a HTTP request to view the details of a channel the user
    is part of
    Parameters:
        url
        token (str)
        channel_id (int)
    Returns:
        JSON data returned from request
    """
    channel_details_info = {
        "token": token,
        "channel_id": channel_id,
    }

    return requests.get(f"{url}/channel/details", params=channel_details_info)


def http_channel_invite(url, token, channel_id, u_id):
    """
    Function that makes a HTTP request for user to invite another
    to the channel
    Parameters:
        url
        token (str)
        channel_id (int)
        u_id (int)
    Returns:
        JSON data returned from request
    """
    channel_invite_info = {
        "token": token,
        "channel_id": channel_id,
        "u_id": u_id,
    }

    return requests.post(f"{url}/channel/invite", json=channel_invite_info)


def http_channel_join(url, token, channel_id):
    """
    Function that makes a HTTP request for a user to join a channel
    Parameters:
        url
        token (str)
        channel_id (int)
    Returns:
        JSON data returned from request
    """
    channel_join_info = {
        "token": token,
        "channel_id": channel_id,
    }

    return requests.post(f"{url}/channel/join", json=channel_join_info)


def http_channel_leave(url, token, channel_id):
    """
    Function that makes a HTTP request for a user to leave a channel
    Parameters:
        url
        token (str)
        channel_id (int)
    Returns:
        JSON data returned from request
    """
    channel_leave_info = {
        "token": token,
        "channel_id": channel_id,
    }

    return requests.post(f"{url}/channel/leave", json=channel_leave_info)


def http_channel_messages(url, token, channel_id, start):
    """
    Function that makes a HTTP request for a user to view the channel's messages
    Parameters:
        url
        token (str)
        channel_id (int)
        start (int)
    Returns:
        JSON data returned from request
    """
    channel_messages_info = {
        "token": token,
        "channel_id": channel_id,
        "start": start,
    }

    return requests.get(f"{url}/channel/messages", params=channel_messages_info)


def http_channel_removemember(url, token, channel_id, u_id):
    """
    Function that makes a HTTP request for a user to view the channel's messages
    Parameters:
        url
        token (str)
        channel_id (int)
        start (int)
    Returns:
        JSON data returned from request
    """
    channel_removemember_info = {
        "token": token,
        "channel_id": channel_id,
        "u_id": u_id,
    }

    return requests.post(f"{url}/channel/removemember", json=channel_removemember_info)
