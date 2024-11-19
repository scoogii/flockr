"""
auth_login_http_test

Testing that auth_login works with
http implementation
"""


import pytest
import requests
from echo_http_test import url
from conftest_http import user_a, user_b, user_c
from http_auth_functions import http_auth_login, http_auth_logout


def test_loginregister_uid_same_http(url, user_a):
    """
    Test 1 - when a user logs in they get the same u_id returned to them
    """
    http_auth_logout(url, user_a["token"])

    payload = http_auth_login(url, "nbayoungboy@gmail.com", "youngboynba123")
    user_a_login = payload.json()

    assert user_a["u_id"] == user_a_login["u_id"]


def test_unique_token_http(url, user_a, user_b):
    """
    Test 2 - two users should have different/unique tokens returned
    """
    # Set info to pass into server
    http_auth_logout(url, user_a["token"])

    http_auth_logout(url, user_b["token"])

    # Login both users
    payload1 = http_auth_login(url, "nbayoungboy@gmail.com", "youngboynba123")
    payload2 = http_auth_login(url, "jerrychan@gmail.com", "w89rfh@fk")

    user_a_login = payload1.json()
    user_b_login = payload2.json()

    assert user_a_login["token"] != user_b_login["token"]


def test_login_incorrect_password_http(url):
    """
    Test 3 - password doesn't match what user registered with -> error
    """
    payload = http_auth_login(url, "jamalmurray27@gmail.com", "nuggetsInFive40")
    assert payload.status_code == 400


def test_login_invalid_user_http(url):
    """
    Test 4 - email doesn't belong to a registerd user -> error
    """
    payload = http_auth_login(url, "idontexist@gmail.com", "secret")
    assert payload.status_code == 400


def test_login_invalid_email_http(url):
    """
    Test 5 - email doesn't belong to a registerd user and is of invalid format -> error
    """
    payload = http_auth_login(url, "abc.com", "noat@email")
    assert payload.status_code == 400
