"""
http_channels_functions

HTTP functions of channels functions for testing
"""


import requests


def http_channels_list(url, token):
    """
    Function that makes a HTTP request to list the channels the user is
    currently part of
    Parameters:
        url
        token (str)
    Returns:
        JSON data returned from request
    """
    channels_list_info = {"token": token}
    return requests.get(f"{url}/channels/list", params=channels_list_info)


def http_channels_listall(url, token):
    """
    Function that makes a HTTP request to list all channels in Flockr
    Parameters:
        url
        token (str)
    Returns:
        JSON data returned from request
    """
    channels_listall_info = {"token": token}
    return requests.get(f"{url}/channels/listall", params=channels_listall_info)


def http_channels_create(url, token, name, is_public):
    """
    Function that makes a HTTP reqeust to create a channel
    Parameters:
        url
        token (str)
        name (str)
        is_public (bool)
    Returns:
        JSON data returned from request
    """
    channel_create_info = {
        "token": token,
        "name": name,
        "is_public": is_public,
    }

    return requests.post(f"{url}/channels/create", json=channel_create_info)
