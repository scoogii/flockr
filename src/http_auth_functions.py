"""
http_auth_functions

HTTP functions of auth functions for testing
"""


import requests


def http_auth_login(url, email, password):
    """
    Function that makes a HTTP request to log the user in
    Flockr
    """
    user_login_info = {
        "email": email,
        "password": password
    }

    return requests.post(f"{url}/auth/login", json=user_login_info)


def http_auth_logout(url, token):
    """
    Function that makes a HTTP request to log the user out
    of Flockr
    Parameters:
        url
        token (str)
    Returns:
        JSON data returned from request
    """
    user_logout_info = {
        "token": token
    }

    return requests.post(f"{url}/auth/logout", json=user_logout_info)


def http_auth_register(url, email, password, name_first, name_last):
    """
    Function that makes a HTTP request to register a user to Flockr
    """
    user_info = {
        "email": email,
        "password": password,
        "name_first": name_first,
        "name_last": name_last,
    }

    return requests.post(f"{url}/auth/register", json=user_info)


def http_auth_passwordreset_request(url, email):
    """
    Function that makes a HTTP request to send a password reset request
    for the user
    Parameters:
        email (str)
    Returns:
        JSON data returned from request
    """
    user_email = {"email": email}

    return requests.post(f"{url}/auth/passwordreset/request", json=user_email)


def http_auth_passwordreset_reset(url, reset_code, new_password):
    """
    Function that makes a HTTP request that resets the password for the user
    Parameters:
        reset_code (int)
        new_password (str)
    Returns:
        JSON data returned from request
    """
    user_reset_info = {
        "reset_code": reset_code, 
        "new_password": new_password
    }

    return requests.post(f"{url}/auth/passwordreset/reset", json=user_reset_info)
