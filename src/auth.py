"""
auth.py
authentication and authorisation
"""


import hashlib
import jwt
import time
from error import InputError
from data import DATA
from auth_helper import (
    check_email_format,
    check_email_unique,
    check_password,
    check_name,
    check_valid_user_email,
    check_valid_reset_code,
    create_handle,
    encode_token,
    decode_token,
    create_user,
    authenticate,
)
from find import find_user_from_token


########################################################################
#                           Main Functions                             #
########################################################################


def auth_login(email, password):
    """
    Generates a valid token for the user to remain authenticated
    Parameters:
        email (str): entered by user
        password (str): entered by user
    Returns: (dict)
        token (str): using jwt
        u_id (int)
    """

    # Check email has valid format
    check_email_format(email)

    # Hashing the password
    password = hashlib.sha256(password.encode()).hexdigest()

    # Checks if the email exists and if so the password also matches the user
    user = authenticate(email, password)

    u_id = user["u_id"]
    # Adding token back to DATA
    user["token"] = str(u_id)

    # Generate the unique # for the token
    token = encode_token(u_id)

    return {
        "u_id": u_id,
        "token": token,
    }


def auth_logout(token):
    """
    Logs a user out by invalidating an active token
    Parameters:
        token (str)
    Returns: (dict)
        is_success (bool)
    """
    # Check token is valid jwt
    decoded_token = decode_token(token)

    # AccessError if token passed in is not a valid token
    find_user_from_token(decoded_token)

    is_success = False
    for user in DATA["users"]:
        if user["token"] == decoded_token:
            # remove token
            user["token"] = ""
            is_success = True

    return { "is_success": is_success }


def auth_register(email, password, name_first, name_last):
    """
    Returns all information about a new user in a dictionary
    Parameters:
        email (str): email entered by user
        password (str): password entered by user
        name_first (str): first name entered by user
        name_last (str): last name entered by user
    Returns: (dict)
        u_id (int)
        token (str): using jwt
    """
    # InputError Checks
    # Check email has valid format
    check_email_format(email)

    # Check email hasn't been taken by another user
    check_email_unique(email)

    # Check password is valid (>6 characters)
    check_password(password)

    # Check first and last name are valid length
    check_name(name_first)
    check_name(name_last)

    # Hashing the password
    password = hashlib.sha256(password.encode()).hexdigest()

    # All input to register is valid -> add the user to DATA
    new_user = create_user(email, password, name_first, name_last)
    DATA["users"].append(new_user)

    u_id = new_user["u_id"]
    # Call function to encode token using jwt
    token = encode_token(u_id)

    return {
        "u_id": u_id,
        "token": token,
    }


def auth_passwordreset_request(email):
    # Check if the email exists -> return user associated with email
    user = check_valid_user_email(email)

    # Creates a unique reset code based on the email of the user and the current time
    code = email + str(time.time())
    # Encode the reset_code to make it more complex
    reset_code = hashlib.sha256(code.encode()).hexdigest()

    user["reset_code"] = reset_code

    # Return reset_code to be sent via email
    return reset_code


def auth_passwordreset_reset(reset_code, new_password):
    # Check the reset code exists
    user = check_valid_reset_code(reset_code)
    # Check new password is valid
    check_password(new_password)

    # Encode and set the new password
    user["password"] = hashlib.sha256(new_password.encode()).hexdigest()

    # Invalidate the reset_code
    user["reset_code"] = None

    return {}
