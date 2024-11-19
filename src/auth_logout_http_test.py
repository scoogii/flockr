"""
auth_logout_http_test

Testing that auth_logout works with
http implementation
"""


import pytest
import requests
from echo_http_test import url
from conftest_http import user_a, user_b, user_c
from http_auth_functions import http_auth_login, http_auth_logout


def test_logout_success(url, user_a):
    """
    Test 1 - A simple test that the success of logging out (returns True)
    """
    payload = http_auth_logout(url, user_a["token"])
    user_a_logout = payload.json()

    assert user_a_logout == {"is_success" : True}


def test_double_logout(url, user_b):
    """
    Test 2 - Checks a token has been invalidated so the user cannot logout if already logged out
    """
    # Logout for the first time -> Success (True)
    http_auth_logout(url, user_b["token"])
    
    # Logout again -> Unsuccessful (False)
    payload = http_auth_logout(url, user_b["token"])

    assert payload.status_code == 400


def test_login_logout_loop_http(url, user_c):
    """
    Test 3 - Tests the functionality of auth_login and auth_logout
    """
    # Get the token of user_c to logout
    http_auth_logout(url, user_c["token"])
    
    # Log back in again 
    http_auth_login(url, "jamalmurray27@gmail.com", "NuggetsInFive41")

    # Logout
    payload = http_auth_logout(url, user_c["token"])
    user_c_logout = payload.json()
    
    assert user_c_logout == {"is_success" : True}


def test_invalid_token_http_1(url):
    """
    Test 4.1 - Checks that invalid tokens will return False (jwt)
    """
    invalid_token_jwt = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbiI6IjEyMzQ1Njc4OTAiLCJuYW1lIjoiSm9obiBEb2UiLCJpYXQiOjE1MTYyMzkwMjJ9.yQhDqJwebPDdPWJZmylK9muvDva7nj0ZQTR6bguYlWs'
    payload = http_auth_logout(url, invalid_token_jwt)
    assert payload.status_code == 400


def test_invalid_token_http_2(url):
    """
    Test 4.2 - Checks that invalid tokens will return False (string)
    """
    invalid_token_str = ""
    payload = http_auth_logout(url, invalid_token_str)

    assert payload.status_code == 400


def test_invalid_token_http_3(url):
    """
    Test 4.3 - Checks that invlaid tokens will return False (int)
    """
    invalid_token_int = 459
    payload = http_auth_logout(url, invalid_token_int)

    assert payload.status_code == 400
