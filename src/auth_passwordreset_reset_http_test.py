import pytest
import requests
from echo_http_test import url
from data import DATA
import time
import imaplib
import email
from http_auth_functions import (
    http_auth_login,
    http_auth_passwordreset_request,
    http_auth_passwordreset_reset,
    http_auth_logout,
)


def read_email_for_code():
    # Parts of method from: https://www.devdungeon.com/content/read-and-send-email-python
    try:
        # Connect and login to IMAP mail server
        username = 'grapefruit1531@gmail.com'
        password = "throwitoutthewindow"
        mail_server = "imap.gmail.com"
        imap_server = imaplib.IMAP4_SSL(host=mail_server)
        imap_server.login(username, password)

        # Choose the Inbox (folder) to search
        imap_server.select('INBOX')

        search_criteria = 'ALL'
        message_numbers_raw = imap_server.search(None, search_criteria)
        message_numbers = message_numbers_raw[1][0].split()

        # Fetch most recent message based on numbers obtained from search
        message_data = (imap_server.fetch(message_numbers[-1], '(RFC822)'))[1]

        message = str(message_data[0][1])
        # Reset_Code will be taken after
        spl_word = 'is: '
        code = message.partition(spl_word)[2]
        # Removes additional characters \r\n
        code = code[:-5]

        imap_server.close()
        imap_server.logout()
        return code

    except Exception as e:
        print(e)


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

    # Registers user_a
    payload = requests.post(f"{url}/auth/register", json=user_a_info).json()

    return {
        "u_id": payload["u_id"],
        "email": "grapefruit1531@gmail.com"
    }


@pytest.fixture
def user_b(url):
    """
    Fixture that gives us user_b's details to use
    """
    user_b_info = {
        "email": "grapefruit1531@gmail.com",
        "password": "w89rfh@fk",
        "name_first": "Jerry",
        "name_last": "Chan",
    }

    payload = requests.post(f"{url}/auth/register", json=user_b_info).json()

    return {
        "u_id": payload["u_id"],
        "email": "grapefruit1531@gmail.com"
    }


def test_passwordreset_reset_success_1_http(url, user_a):
    '''
    Test 1 - Tests success by logging in with new password
    '''
    http_auth_passwordreset_request(url, "grapefruit1531@gmail.com")

    reset_code = read_email_for_code()

    # Reset the password
    http_auth_passwordreset_reset(url, reset_code, "youngboynba321")

    # Login with new password and check if successful
    payload = http_auth_login(url, "grapefruit1531@gmail.com", "youngboynba321")
    user_a_login = payload.json()

    u_id_1 = user_a["u_id"]

    assert u_id_1 == user_a_login["u_id"]


def test_passwordreset_reset_success_2_http(url, user_a):
    '''
    Test 2 - Test success in password change if user can no longer login with original password
    '''
    http_auth_passwordreset_request(url, "grapefruit1531@gmail.com")

    reset_code = read_email_for_code()

    # Reset the password
    http_auth_passwordreset_reset(url, reset_code, "jebrevjebkviwfr84fh")

    # Failure to login with old password
    payload = http_auth_login(url, "grapefruit1531@gmail.com", "w89rfh@fk")

    assert payload.status_code == 400


def test_passwordreset_reset_success_3_http(url, user_a):
    '''
    Test 3 - User can request code multiple times but only most recent can be used to change password
    '''
    http_auth_passwordreset_request(url, "grapefruit1531@gmail.com")
    reset_code_1 = read_email_for_code()

    # Second request to change password
    http_auth_passwordreset_request(url, "grapefruit1531@gmail.com")
    reset_code_2 = read_email_for_code()

    # Reset the password with old code
    payload_1 = http_auth_passwordreset_reset(url, reset_code_1, "newpassword")

    assert payload_1.status_code == 400

    # Reset the password with newest code
    payload_2 = http_auth_passwordreset_reset(url, reset_code_2, "newpassword")

    assert payload_2.status_code == 200

# Input Errors
def test_passwordreset_invalid_password_http(url, user_a):
    '''
    Test 4 - Reset code is valid but password is too short -> InputError
    '''
    http_auth_passwordreset_request(url, "grapefruit1531@gmail.com")
    reset_code = read_email_for_code()

    # Attempt to reset with invalid password
    payload = http_auth_passwordreset_reset(url, reset_code, "short")

    assert payload.status_code == 400


def test_passwordreset_invalid_code_http(url):
    '''
    Test 5 - Reset code doesn't exist -> InputError
    '''
    reset_code = 'invalidresetcode'

    # Attempt to reset with non-existant reset code -> error
    payload = http_auth_passwordreset_reset(url, reset_code, "jsblifsvbf")

    assert payload.status_code == 400
