"""
http_user_functions

HTTP functions of user functions for testing
"""


import requests


def http_user_profile(url, token, u_id):
    """
    Function that makes a HTTP request to retrieve
    user profile
    Parameters:
        url
        token (str)
        u_id (int)
    Returns:
        JSON returned data from request
    """
    user_profile_info = {
        "token": token,
        "u_id": u_id,
    }

    return requests.get(f"{url}/user/profile", params=user_profile_info)


def http_user_profile_setname(url, token, name_first, name_last):
    """
    Function that makes a HTTP request to update
    user's name
    Parameters:
        url
        token (str)
        name_first (str)
        name_last(str)
    Returns:
        JSON returned data from request
    """
    user_setname_info = {
        "token": token,
        "name_first": name_first,
        "name_last": name_last,
    }

    return requests.put(f"{url}/user/profile/setname", json=user_setname_info)


def http_user_profile_setemail(url, token, email):
    """
    Function that makes a HTTP request to update
    user's email
    Parameters:
        url
        token (str)
        email (str)
    Returns:
        JSON returned data from request
    """
    user_setemail_info = {
        "token": token,
        "email": email,
    }

    return requests.put(f"{url}/user/profile/setemail", json=user_setemail_info)


def http_user_profile_sethandle(url, token, handle_str):
    """
    Function that makes a HTTP request to update
    user's handle
    Parameters:
        url
        token (str)
        handle_str (str)
    Returns:
        JSON returned data from request
    """
    user_sethandle_info = {
        "token": token,
        "handle_str": handle_str,
    }

    return requests.put(f"{url}/user/profile/sethandle", json=user_sethandle_info)


def http_user_profile_uploadphoto(url, token, img_url, x_start, y_start, x_end, y_end):
    """
    Function that makes a HTTP request to upload
    a profile picture
    Parameters:
        url
        token (str)
        img_url (str)
        x_start (int)
        y_start (int)
        x_end (int)
        y_end (int)
    Returns:
        JSON returned data from request
    """
    user_uploadphoto_info = {
        "token": token,
        "img_url": img_url,
        "x_start": x_start,
        "y_start": y_start,
        "x_end": x_end,
        "y_end": y_end,
    }

    return requests.post(f"{url}/user/profile/uploadphoto", json=user_uploadphoto_info)
