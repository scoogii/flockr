"""
other.py
clearing DATA, showing all users,
changing admin permissions, and searching for messages
"""


from data import DATA
from error import InputError, AccessError
from auth import decode_token
from find import find_user_from_token, find_user_from_uid, find_uid_from_token


########################################################################
#                          Auxillary Functions                         #
########################################################################


# Check if p_id is valid
def check_valid_pid(permission_id):
    """
    Check if p_id is valid
    Parameters:
        permission_id (str)
    Return:
        (bool): "True" is permission_id is valid or "False" is not
    """
    if permission_id in (1, 2):
        return True
    return False


# Check if that user (w/ token) is authorised owner
def check_is_admin(token):
    """
    Check if user is authorised owner with token
    Parameters:
        token (str)
    Return:
        (bool): "True" if the user is an admin or "False" if not
    """
    for user in DATA["users"]:
        if user["token"] == token:
            if user["permission_id"] == 1:
                return True
    return False


########################################################################
#                           Main Functions                             #
########################################################################


def clear():
    """
    Clear DATA after test function is complete
    """
    DATA["users"].clear()
    DATA["channels"].clear()
    DATA["message_log"]["messages"].clear()
    DATA["message_log"]["msg_counter"] = 1
    DATA["standup"].clear()

def users_all(token):
    """
    Returns a list of all users and their associated details
    Parameters:
        token (str)
    Return:
        users (dictionary)
    """
    decoded_token = decode_token(token)
    find_user_from_token(decoded_token)

    # Create a dictionary that will contain all channels
    all_users = {"users": []}

    # Loop through all channels and add details to channels_all
    for user in DATA["users"]:
        all_users["users"].append(
            {
                "u_id": user["u_id"],
                "email": user["email"],
                "name_first": user["name_first"],
                "name_last": user["name_last"],
                "handle_str": user["handle_str"],
                "profile_img_url": user["profile_img_url"],
            }
        )

    return all_users


def admin_userpermission_change(token, u_id, permission_id):
    """
    Given a User by their user ID, set their permissions to new permissions
    described by permission_id

    Parameters:
        token (str)
        u_id (int)
        permission_id (int)
    InputError:
        - u_id does not refer to a valid user
        - permission_uid does not refer to a value permission
    AccessError:
        - The authorised user is not an owner
    Return:
        {}
    """
    decoded_token = decode_token(token)

    # InputError: Check if the UID is valid by trying to find it
    find_user_from_token(decoded_token)

    # AccessError: Check if the token is valid by trying to find it
    find_user_from_uid(u_id)

    # InputError: Check if the PID is valid (1 or 2)
    # Also check valid token
    if not check_valid_pid(permission_id):
        raise InputError(description="Invalid Permission ID")

    # Check if the user is admin of flockr first
    if not check_is_admin(decoded_token):
        raise AccessError(description="User is not an admin")

    user = find_user_from_uid(u_id)
    user["permission_id"] = permission_id


def search(token, query_str):
    """
    Given a query string, return a collection of messages that match the query string
    in all of the channels that the user has joined.

    Parameters:
        token (str)
        query_str (str)
    Return:
        messages (dict)
    """
    decoded_token = decode_token(token)
    u_id = find_uid_from_token(decoded_token)

    message_match = []
    for user_m_id in DATA["users"][u_id - 1]["user_message_id"]:
        for message in DATA["message_log"]["messages"]:
            if message["message_id"] == user_m_id and query_str in message["message"]:
                message_match.append(message)

    # For each message being returned, check whether or not the user calling search
    # has reacted to each message
    for message in message_match:
        if u_id in message["reacts"][0]["u_ids"]:
            message["reacts"][0]["is_this_user_reacted"] = True
        else:
            message["reacts"][0]["is_this_user_reacted"] = False

    return {"messages": message_match}
