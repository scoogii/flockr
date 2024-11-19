"""
auth_passwordreset_request_http_test

Testing that auth_passwordreset_request works with
http implementation
"""


import pytest
import requests
import time
from echo_http_test import url
from auth_passwordreset_reset_http_test import read_email_for_code
from http_auth_functions import http_auth_passwordreset_request


@pytest.fixture
def user_a(url):
    """
    Fixture that gives us user_a's details to use
    """
    user_a_info = {
        "email": "grapefruit1531@gmail.com",
        "password": "youngboynba123",
        "name_first": "Kentrell",
        "name_last": "Gaulden",
    }

    payload = requests.post(f"{url}/auth/register", json=user_a_info).json()

    return {
        "token": payload["token"],
        "u_id": payload["u_id"],
        "email": user_a_info["email"]
    }


def test_passwordreset_request_success_http_1(url, user_a):
    '''
    Test 1 - Checking success by asserting the response
    '''
    payload = http_auth_passwordreset_request(url, user_a["email"])

    # Code would be emailed to user and return {}
    assert payload.json() == {}


def test_passwordreset_request_multiple_1(url, user_a):
    '''
    Test 2 - Requesting multiple secret reset codes is allowed and checking success by status_code
    '''
    http_auth_passwordreset_request(url, user_a["email"])
    http_auth_passwordreset_request(url, user_a["email"])
    http_auth_passwordreset_request(url, user_a["email"])

    payload = http_auth_passwordreset_request(url, user_a["email"])

    # Code would be emailed to user and return {}
    assert payload.status_code == 200


def test_passwordreset_request_http_multiple_2(url, user_a):
    '''
    Test 3 - Checking code is unique when a request is sent multiple times by a user
    '''
    # First request to change password
    http_auth_passwordreset_request(url, user_a["email"])
    reset_code_1 = read_email_for_code()

    # Second request to change password
    http_auth_passwordreset_request(url, user_a["email"])
    reset_code_2 = read_email_for_code()

    assert reset_code_1 != reset_code_2


# InputError
def test_passwordreset_request_http_invalidemail(url):
    '''
    Test 4 - When an email is not found it raises an error
    '''
    invalid_email = "idontexist@gmail.com"
    payload = http_auth_passwordreset_request(url, invalid_email)
    assert payload.status_code == 400
