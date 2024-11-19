"""
http_standup_functions

HTTP functions of standup functions for testing
"""


import requests


def http_standup_active(url, token, channel_id):
    """
    Function that makes a HTTP request to check the status
    of a standup in a channel
    Parameters:
        url
        token (str)
        channel_id (int)
    Returns:
        JSON data returned from request
    """
    standup_active_info = {
        "token": token,
        "channel_id": channel_id
    }

    return requests.get(f"{url}/standup/active", params=standup_active_info)


def http_standup_send(url, token, channel_id, message):
    """
    Function that makes a HTTP request to send messages during
    a standup in a channel
    Parameters:
        url
        token (str)
        channel_id (int)
        message (str)
    Returns:
        JSON data returned from request
    """
    standup_send_info = {
        "token": token,
        "channel_id": channel_id,
        "message": message
    }

    return requests.post(f"{url}/standup/send", json=standup_send_info)


def http_standup_start(url, token, channel_id, length):
    """
    Function that makes a HTTP request to start a standup
    within a given channel
    Parameters:
        url
        token (str)
        channel_id (int)
        length (int)
    Returns:
        JSON data returned from request
    """
    standup_start_info = {
        "token": token,
        "channel_id": channel_id,
        "length": length
    }

    return requests.post(f"{url}/standup/start", json=standup_start_info)
