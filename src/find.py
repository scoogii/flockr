"""
find.py
find functions used in various files are sourced from here
"""


from data import DATA
from error import InputError, AccessError


# _____________________________Find token______________________________#


def find_uid_from_token(token):
    """
    Finds the uid of a user from the token passed in
    Parameters:
        token (str)
    Returns:
        user["u_id"] (int): if token match is found, otherwise
        raise AccessError for invalid user token
    """
    for user in DATA["users"]:
        if user["token"] == token:
            return user["u_id"]

    raise AccessError(description="Invalid Token")


# ______________________________Find User______________________________#


def find_user_from_token(token):
    """
    Finds the user from the token passed in
    Parameters:
        token (str)
    Returns:
        user (dictionary): contains all the details of the user
        otherwise nothing if token match is not found
    """
    for user in DATA["users"]:
        if user["token"] == token:
            return user

    raise AccessError(description="Invalid Token")


def find_user_from_uid(u_id):
    """
    Finds the user profile from a given user ID
    Parameters:
        u_id (int): the user's unique ID
    Returns:
        user (dict): details of the user
    """
    for user in DATA["users"]:
        if user["u_id"] == u_id:
            return user

    raise InputError(description="Invalid User ID")


# ____________________________Find cid from mid________________________________#


def find_cid_from_mid(m_id):
    """
    Finds the channel_id of a user from message_id passed in
    Parameters:
        m_id (int)
    Returns:
        channel["channel_id"], otherwise if not found then False
    """
    for channel in DATA["channels"]:
        for message_id in channel["messages"]:
            if message_id == m_id:
                m_id_match = channel["channel_id"]

    return m_id_match
