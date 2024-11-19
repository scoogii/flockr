"""
http_message_functions

HTTP functions of message functions for testing
"""


import requests


def http_message_send(url, token, channel_id, message):
    """
    Function that makes a HTTP request to send a message to
    a channel
    Parameters:
        url
        token (str)
        channel_id (int)
        message (str)
    Returns:
        m_id (int)
    """
    message_send_info = {
        "token": token,
        "channel_id": channel_id,
        "message": message,
    }

    return requests.post(f"{url}/message/send", json=message_send_info)


def http_message_remove(url, token, m_id):
    """
    Function that makes a HTTP request to remove a message
    from a channel
    Parameters:
        url
        token (str)
        m_id (int)
    Returns:
        None
    """
    message_remove_info = {
        "token": token,
        "message_id": m_id,
    }

    return requests.delete(f"{url}/message/remove", json=message_remove_info)


def http_message_edit(url, token, m_id, message):
    """
    Function that makes a HTTP request to edit a message in
    a channel
    Parameters:
        url
        token (str)
        m_id (int)
        message (str)
    Returns:
        None
    """
    message_edit_info = {
        "token": token,
        "message_id": m_id,
        "message": message,
    }

    return requests.put(f"{url}/message/edit", json=message_edit_info)


def http_message_sendlater(url, token, channel_id, message, time_sent):
    """
    Function that makes a HTTP request to send a message later in
    a channel
    Parameters:
        url
        token (str)
        channel_id (int)
        message (str)
        time_sent (int)
    Returns:
        m_id (int)
    """
    message_sendlater_info = {
        "token": token,
        "channel_id": channel_id,
        "message": message,
        "time_sent": time_sent,
    }

    return requests.post(f"{url}/message/sendlater", json=message_sendlater_info)


def http_message_react(url, token, m_id, react_id):
    """
    Function that makes a HTTP request to react to a message
    in a channel
    Parameters:
        url
        token (str)
        m_id (int)
        react_id (int)
    Returns:
        None
    """
    message_react_info = {
        "token": token,
        "message_id": m_id,
        "react_id": react_id,
    }

    return requests.post(f"{url}/message/react", json=message_react_info)


def http_message_unreact(url, token, m_id, react_id):
    """
    Function that makes a HTTP request to unreact to a message
    in a channel
    Parameters:
        url
        token (str)
        m_id (int)
        react_id (int)
    Returns:
        None
    """
    message_unreact_info = {
        "token": token,
        "message_id": m_id,
        "react_id": react_id,
    }

    return requests.post(f"{url}/message/unreact", json=message_unreact_info)


def http_message_pin(url, token, m_id):
    """
    Function that makes a HTTP request to pin a message
    in a channel
    Parameters:
        token (str)
        m_id (int)
    Returns:
        None
    """
    message_pin_info = {
        "token": token,
        "message_id": m_id,
    }

    return requests.post(f"{url}/message/pin", json=message_pin_info)


def http_message_unpin(url, token, m_id):
    """
    Function that makes a HTTP request to unpin a message
    in a channel
    Parameters:
        token (str)
        m_id (int)
    Returns:
        None
    """
    message_unpin_info = {
        "token": token,
        "message_id": m_id,
    }

    return requests.post(f"{url}/message/unpin", json=message_unpin_info)
