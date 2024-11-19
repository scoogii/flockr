"""
user_profile_uploadphoto_http_test

Testing that user_profile_uploadphoto works with
HTTP implementation
"""


import requests
import pytest
from auth import encode_token
from echo_http_test import url
from conftest_http import user_a, user_b
from http_user_functions import http_user_profile, http_user_profile_uploadphoto


def test_user_profile_uploadphoto_http_success(url, user_a):
    """
    Test 1 - Testing a profile photo image has been successfully
    uploaded
    """
    # Send post request to update photo
    img_url = "https://i.stack.imgur.com/34AD2.jpg"
    http_user_profile_uploadphoto(url, user_a["token"], img_url, 0, 0, 240, 240)

    # Retrieve user profile to check photo url
    payload = http_user_profile(url, user_a["token"], user_a["u_id"])
    result = payload.json()

    filename = "src/static/" + encode_token(user_a["token"])[40:50] + str(user_a["u_id"]) + ".jpg"
    assert result == {
        "user": {
            "u_id": 1,
            "email": "nbayoungboy@gmail.com",
            "name_first": "Kentrell",
            "name_last": "Gaulden",
            "handle_str": "kentrellgaulden",
            "profile_img_url": url + filename
        }
    }


def test_user_profile_uploadphoto_http_invalid_format(url, user_a):
    """
    Test 2 - System Error - Image uploaded is not a JPG
    """
    img_url = "https://www.freeiconspng.com/thumbs/profile-icon-png/profile-icon-9.png"
    payload = http_user_profile_uploadphoto(url, user_a["token"], img_url, 0, 0, 860, 663)

    # System Error - Invalid format
    assert payload.status_code == 400


def test_user_profile_uploadphoto_http_dimension_one(url, user_b):
    """
    Test 3 - System Error - Invalid Dimension
    """
    img_url = "https://i.stack.imgur.com/34AD2.jpg"
    payload = http_user_profile_uploadphoto(url, user_b["token"], img_url, 0, 0, 360, 360)

    # System Error - Invalid dimensions provided by user
    assert payload.status_code == 400


def test_user_profile_uploadphoto_http_invalidtoken(url, user_b):
    """
    Test 4 - System Error - Invalid Token
    """
    img_url = "https://i.stack.imgur.com/34AD2.jpg"
    payload = http_user_profile_uploadphoto(url, "randomtoken", img_url, 0, 0, 240, 240)

    # System Error - Invalid token provided
    assert payload.status_code == 400


def test_user_profile_uploadphoto_http_invalid_status_code(url, user_b):
    """
    Test 5 - System Error - Invalid HTTP status code
    """
    img_url = "https://mwave.com.au/myaccount"
    payload = http_user_profile_uploadphoto(url, user_b["token"], img_url, 0, 0, 240, 240)

    # System Error - Invalid HTTP status code
    assert payload.status_code == 400
