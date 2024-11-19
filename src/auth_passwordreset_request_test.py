"""
auth/passwordreset/request
Description: Given an email address, if the user is a registered user, 
send's them a an email containing a specific secret code
Parameters (email)
"""

import pytest
from auth import auth_register, auth_login, auth_logout, auth_passwordreset_request, auth_passwordreset_reset
from error import InputError
from other import clear
from conftest import user_a
from time import sleep

def test_passwordreset_request_unique(user_a):
    """
    Test 1 - Checking both request and reset
    """   
    reset_code_1 = auth_passwordreset_request("nbayoungboy@gmail.com")
    sleep(0.2)
    reset_code_2 = auth_passwordreset_request("nbayoungboy@gmail.com")

    assert reset_code_1 != reset_code_2

    clear()


def test_password_request_invalid_email():
    """
    Test 2 - Invalid email so cannot request a reset_code
    """
    with pytest.raises(InputError, match=r"Email does not exist"):
        auth_passwordreset_request("abc@gmail.com")

    clear()


def test_password_request_invalid_email_empty(user_a):
    """
    Test 3 - Invalid email so cannot request a reset_code
    """
    with pytest.raises(InputError, match=r"Email does not exist"):
        auth_passwordreset_request("")

    clear()