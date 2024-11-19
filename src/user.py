"""
user.py
Displays profile, sets new names, emails
and handles
"""

import requests
from PIL import Image
from flask import request
from auth import encode_token, decode_token
from auth_helper import (
    check_email_format,
    check_email_unique,
    check_name,
    check_handle_unique,
    check_handle_valid,
    check_valid_http_status,
    check_if_jpeg,
    check_img_dimension_valid,
)
from find import find_user_from_token, find_user_from_uid


########################################################################
#                           Main Functions                             #
########################################################################


def user_profile(token, u_id):
    """
    Returns information about user with u_id
    Parameters:
        token (str): the user's unique token
        u_id (int):
    Returns:
        user (dict): details of the user (u_id) that was requested by another user (token)
    """
    decoded_token = decode_token(token)
    find_user_from_token(decoded_token)
    user = find_user_from_uid(u_id)

    return {
        "user": {
            "u_id": user["u_id"],
            "email": user["email"],
            "name_first": user["name_first"],
            "name_last": user["name_last"],
            "handle_str": user["handle_str"],
            "profile_img_url": user["profile_img_url"]
        },
    }


def user_profile_setname(token, name_first, name_last):
    """
    Changing name of user
    Parameters:
        token (str): the user's unique token
        name_first (str):
        name_last (str)
    Returns:
        dict: (empty)
    """
    decoded_token = decode_token(token)
    check_name(name_first)
    check_name(name_last)

    user = find_user_from_token(decoded_token)
    user["name_first"] = name_first
    user["name_last"] = name_last

    return {}


def user_profile_setemail(token, email):
    """
    Changing email of user
    Parameters:
        token (str): the user's unique token
        email (str)
    Returns:
        dict: (empty)
    """
    decoded_token = decode_token(token)
    check_email_format(email)
    check_email_unique(email)

    user = find_user_from_token(decoded_token)
    user["email"] = email.lower()

    return {}


def user_profile_sethandle(token, handle_str):
    """
    Changing handle of user
    Parameters:
        token (str): the user's unique token
        handle (str)
    Returns:
        dict: (empty)
    """
    decoded_token = decode_token(token)
    check_handle_valid(handle_str)
    check_handle_unique(handle_str)

    user = find_user_from_token(decoded_token)
    user["handle_str"] = handle_str

    return {}


def user_profile_uploadphoto(token, img_url, x_start, y_start, x_end, y_end):
    """
    Given a URL of an image, crops the image within bounds
    Parameters:
        token (str): the user's unique token
        img_url (str)
        x_start (int)
        y_start (int)
        x_end (int)
        y_end (int)
    Returns:
        dict: (empty)
    """
    decoded_token = decode_token(token)
    check_valid_http_status(img_url)
    check_if_jpeg(img_url)
    check_img_dimension_valid(img_url, x_start, y_start, x_end, y_end)

    # Grab image from internet
    payload = requests.get(img_url, stream=True)
    payload.raw.decode_content = True

    # Crop and image if necessary
    image = Image.open(payload.raw)
    crop_area = (x_start, y_start, x_end, y_end)
    image_cropped = image.crop(crop_area)

    # Save image and assign url
    user = find_user_from_token(decoded_token)
    filename = "src/static/" + encode_token(user["token"])[40:50] + str(user["u_id"]) + ".jpg"
    image_cropped.save(filename)
    user["profile_img_url"] = request.host_url + filename

    return {}
