"""
http_other_functions

HTTP functions of other functions for testing
"""


import requests


def http_admin_userpermission_change(url, token, u_id, permission_id):
    """
    Function that makes a HTTP request to change admin permissions
    in a channel
    Parameters:
        token (str)
        u_id (int)
        permission_id (int)
    Returns:
        None
    """
    admin_userpermission_change_info = {
        "token": token,
        "u_id": u_id,
        "permission_id": permission_id,
    }

    return requests.post(f"{url}/admin/userpermission/change", json=admin_userpermission_change_info)


def http_search(url, token, query_str):
    """
    Function that makes a HTTP request to search for messages
    that contain a given query string
    Parameters:
        url
        token (str)
        query_str (str)
    Returns:
        messages (dict)
    """
    search_info = {
        "token": token,
        "query_str": query_str,
    }

    return requests.get(f"{url}/search", params=search_info)


def http_clear(url):
    """
    Function that makes a HTTP request to clear data
    Parameters:
        None
    Returns:
        None
    """

    return requests.delete(f"{url}/clear")


def http_users_all(url, token):
    """
    Function that makes a HTTP request to grab a list
    of all users and their details
    Parameters:
        url
        token (str)
    Returns:
        users (list)
    """
    users_all_info = {
        "token": token
    }

    return requests.get(f"{url}/users/all", params=users_all_info)
