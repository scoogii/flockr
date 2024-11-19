"""
user_profile_uploadphoto_test

Testing that helper functions for user_profile_uploadphoto
raise the correct errors
"""


import pytest
from auth import auth_register
from auth_helper import (
    check_valid_http_status,
    check_if_jpeg,
    check_img_dimension_valid,
)
from error import InputError
from other import clear
from conftest import user_a


def test_user_profile_uploadphoto_valid_dimension(user_a):
    """
    Test 1 - Tests that chosen dimensions are valid for the given image
    """
    img_url = "https://i.stack.imgur.com/34AD2.jpg"
    x_start = 0
    y_start = 0
    x_end = 5
    y_end = 5

    # Check that the image dimensions are valid and that the http status returns success
    assert check_img_dimension_valid(img_url, x_start, y_start, x_end, y_end) == True
    assert check_valid_http_status(img_url) == True

    clear()


def test_user_profile_uploadphoto_invalid_status(user_a):
    """
    Test 2 - InputError - Invalid HTTP status
    """
    # Provide invalid URL
    img_url = "https://mwave.com.au/myaccount"

    # InputError - invalid status code
    with pytest.raises(InputError, match=r"Invalid HTTP status code"):
        check_valid_http_status(img_url)

    clear()


def test_user_profile_uploadphoto_valid_format(user_a):
    """
    Test 3 - Tests that jpeg image is considered a valid upload
    """
    # Provide valid image in PNG format
    img_url = "https://personal.psu.edu/xqz5228/jpg.jpg"
        
    # Check that the image dimensions are valid and that the http status returns success
    assert check_if_jpeg(img_url) == True
    assert check_valid_http_status(img_url) == True

    clear()


def test_user_profile_uploadphoto_invalid_format(user_a):
    """
    Test 4 - InputError - Invalid Image Format
    """
    # Provide valid image in PNG format
    img_url = "https://www.freeiconspng.com/thumbs/profile-icon-png/profile-icon-9.png"

    with pytest.raises(InputError, match=r"Image uploaded is not a JPG"):
        check_if_jpeg(img_url)

    clear()


def test_user_profile_uploadphoto_invalid_dimension_1(user_a):
    """
    Test 5.1 - InputError - Invalid Dimensions provided - Invalid x_start
    """
    img_url = "https://i.stack.imgur.com/34AD2.jpg"
    x_start = -696969
    y_start = 0
    x_end = 5
    y_end = 5

    with pytest.raises(InputError, match=r"Dimensions provided are invalid"):
        check_img_dimension_valid(img_url, x_start, y_start, x_end, y_end)

    clear()


def test_user_profile_uploadphoto_invalid_dimension_2(user_a):
    """
    Test 5.2 - InputError - Invalid Dimensions provided - Invalid y_start,
    """
    img_url = "https://i.stack.imgur.com/34AD2.jpg"
    x_start = 0
    y_start = -696969
    x_end = 5
    y_end = 5

    with pytest.raises(InputError, match=r"Dimensions provided are invalid"):
        check_img_dimension_valid(img_url, x_start, y_start, x_end, y_end)

    clear()


def test_user_profile_uploadphoto_invalid_dimension_3(user_a):
    """
    Test 5.3 - Input Error - Invalid Dimensions provided - Invalid x_end
    """
    img_url = "https://i.stack.imgur.com/34AD2.jpg"
    x_start = 0
    y_start = 0
    x_end = -696969
    y_end = 5

    with pytest.raises(InputError, match=r"Dimensions provided are invalid"):
        check_img_dimension_valid(img_url, x_start, y_start, x_end, y_end)

    clear()


def test_user_profile_uploadphoto_invalid_dimension_4(user_a):
    """
    Test 5.4 - Input Error - Invalid Dimensions provided - Invalid y_end
    """
    img_url = "https://i.stack.imgur.com/34AD2.jpg"
    x_start = 0
    y_start = 0
    x_end = 5
    y_end = -696969

    with pytest.raises(InputError, match=r"Dimensions provided are invalid"):
        check_img_dimension_valid(img_url, x_start, y_start, x_end, y_end)

    clear()
