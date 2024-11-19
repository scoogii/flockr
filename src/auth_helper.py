"""
auth_helper.py
helper functions for auth.py and user.py are sourced from here
"""


import jwt
import re
import requests
from error import InputError
from data import DATA
from PIL import Image


AUTH_KEY = "grapewindowljwbclwubcixkwdcuiwbsdlxuwscbwlsducbslcbjks"


def check_handle_unique(handle_str):
    """
    Utilises a loop to check if the handle is already in use
    Parameters:
        handle_str as a string
    Returns:
        (bool): True if handle is unique or raise InputError if not
    """

    for user in DATA["users"]:
        if user["handle_str"] == handle_str:
            raise InputError(description="Handle taken by another user")

    return True


def check_handle_valid(handle_str):
    """
    Utilises comparison operators to check if length of handle is valid
    Parameters:
        handle_str as a string
    Returns:
        (bool): True if handle is valid or raise InputError if not
    """

    if len(handle_str) < 2 or len(handle_str) > 20:
        raise InputError(
            description="Handle should be between 2 and 20 characters long"
        )

    return True


def check_email_format(email):
    """
    Uses the regex to check if the email has a valid format
    Parameters:
        email (str): as a string and utilises
    Returns:
        (bool): 'True' if the email is valid or raise an InputError if not
    """
    regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    # Check: Email in valid format
    if not re.search(regex, email):
        raise InputError(description="Email is invalid")


def check_email_unique(email):
    """
    Utilises a loop to check if the email is already in use
    Parameters:
        email (str) as a string and
    Returns:
        (bool): 'True' if the email is unique or raise an InputError if not
    """
    # Check: Email already used
    for user in DATA["users"]:
        if user["email"] == email:
            raise InputError(description="Email taken by another user")

    return True


def check_password(password):
    """
    Validates length of password
    Parameters:
        password (str)
    Returns:
        (bool): 'True' if the password is valid or raise an InputError if not
    """
    if len(password) < 6:
        raise InputError(description="Invalid password; too little characters")

    return True


def check_name(name):
    """
    Uses comparison operators to check for invalid operators as well as len for length
    Parameters:
        name (str): can be first/last name of the user
    Return:
        (bool): 'True' if the name is valid or raises an InputError if not
    """
    # Convert any input into a string first
    name = str(name)

    #  Check if length of name is 1-50 (inclusive)
    if len(name) < 1 or len(name) > 50:
        raise InputError(description="Name must be between 1 and 50 characters inclusive")


def check_valid_http_status(img_url):
    """
    Uses requests library to check if the img_url returns a valid HTTP status code
    Parameters:
        img_url (str): url in string form for image
    Return:
        (bool): 'True' if url returns a valid HTTP status code
    """
    # Retrieve image from internet
    payload = requests.get(img_url, stream = True)

    # Check status code
    if payload.status_code != 200:
        raise InputError(description="Invalid HTTP status code")

    return True


def check_if_jpeg(img_url):
    """
    Uses requests library to check if the image provided is in JPEG format
    Parameters:
        img_url (str): url in string form for image
    Return:
        (bool): 'True' if the image is a valid format
    """
    # Retrieve image from internet
    payload = requests.get(img_url, stream = True)

    # Check image format
    if payload.headers["Content-Type"] != "image/jpeg":
        raise InputError(description="Image uploaded is not a JPG")

    return True


def check_img_dimension_valid(img_url, x_start, y_start, x_end, y_end):
    """
    Uses Image from PIL library as well as requests to find
    image dimensions and check against user input
    Parameters:
        img_url (str): url in string form for image
        x_start (int)
        y_start (int)
        x_end (int)
        y_end (int)
    Return:
        (bool): 'True' if the image is a valid format
    """
    # Retrieve image from internet
    payload = requests.get(img_url, stream = True)
    payload.raw.decode_content = True

    # Retrieve image dimensions
    image = Image.open(payload.raw)

    error = False
    if x_start < 0 or x_start >= image.size[0]:
        error = True
    elif x_end <= 0 or x_end > image.size[0]:
        error = True
    elif y_start < 0 or y_start >= image.size[1]:
        error = True
    elif y_end <= 0 or y_end > image.size[1]:
        error = True

    if error == True:
        raise InputError(description="Dimensions provided are invalid")

    return True


def check_valid_user_email(email):
    '''
    Searches for a user with the email given
    Parameters:
        email (str): entered by user
    Returns: user from data structure if they exist
    if the email does not belong to any user it will raise an error
    '''
    for user in DATA["users"]:
        if user["email"] == email:
            return user
    raise InputError(description="Email does not exist")


def check_valid_reset_code(reset_code):
    '''
    Searches for the reset-code in users
    Parameters:
        reset_code (str): entered by user
    Returns: user who the reset_code belonged to
        - raises InputError if the reset_code doesn't exist
    '''
    for user in DATA['users']:
        if user["reset_code"] == reset_code:
            return user

    raise InputError(description="Invalid password reset code")


def create_handle(name_first, name_last):
    """
    Creates a handle and ensures it is unique
    Parameters:
        name_first (str): The first name entered by user
        name_last (str): The last name entered by user
    Returns:
        handle (str): concatentation of a lowercase-only
                      first name and last name cut-off at 20 characters
    """
    handle = name_first.replace(" ", "") + name_last.replace(" ", "")

    # Change handle to all lowercase
    handle = handle.lower()

    # Ensure handle is under 20 characters
    if len(handle) > 20:
        length = int(len(handle) - 20)
        handle = handle[:len(handle) - length]

    # Check handle is unique
    match = 0
    for user in DATA["users"]:
        while user["handle_str"] == handle:
            # Handle already exists for another user
            match = match + 1
            # Ensure by adding digits handle won"t exceed 20 characters
            if len(handle) > 18:
                length2 = int(len(handle) - 18)
                handle = handle[:len(handle) - length2]
            # Removing any digits from handle
            handle = "".join(filter(lambda character: not character.isdigit(), handle))
            if match < 10:
                handle = handle + "0" + str(match)
            else:
                handle = handle + str(match)

    return handle


def encode_token(uid):
    """
    Returned encoded token to store in DATA structure
    """
    return jwt.encode({"token": str(uid)}, AUTH_KEY, algorithm="HS256").decode("utf-8")


def decode_token(encoded_token):
    """
    Returns decoded token
    """
    try:
        structure = jwt.decode(str(encoded_token).encode("utf-8"), AUTH_KEY, algorithms=["HS256"])
        return str(structure["token"])
    except:
        return "not_a_token"


def create_user(email, password, name_first, name_last):
    """
    Creates a user and returns all information about a new user in a dictionary
    Parameters:
        email (str): email entered by user
        password (str): password entered by user
        name_first (str): first name entered by user
        name_last (str): last name entered by user
    Returns: new_user (dictionary of parameters + token, u_id, handle)
        u_id (int)
        token (str)
        handle (str): concatentation of a lowercase-only first name and last name
    """
    handle = create_handle(name_first, name_last)

    if not DATA["users"]:
        index = 0
        p_id = 1
    else:
        index = len(DATA["users"])
        p_id = 2

    new_user = {
        "email": email,
        "password": password,
        "reset_code": None,
        "name_first": name_first,
        "name_last": name_last,
        "u_id": (index+1),
        "token": str(index+1),
        "handle_str": handle,
        "permission_id": p_id,
        "user_message_id": [],
        "profile_img_url": None
    }
    return new_user


def authenticate(email, password):
    """
    Utilises loops and comparisons to check that the user exists and
    the password matches the one registered with
    Will return the user information if correct
    Parameters:
        email (str): entered by user
        password (str): entered by user
    Returns: (dict)
        user (dict): if the password is valid or
        - raises InputError if not valid password/email
    """
    for user in DATA["users"]:
        if user["email"] == email:
            if user["password"] != password:
                raise InputError(description="Incorrect password")
            return user
    # No user was found with email
    raise InputError(description="Email does not belong to a user")
