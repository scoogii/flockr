'''
auth/passwordreset/reset 
Description: Given a reset code for a user, set that user's new password to the password provided
Parameters: (reset_code, new_password)
Exeptions:
- InputError - reset_code is not a valid reset code
- InputError - Password entered is not a valid password
'''


import pytest
from auth import auth_register, auth_login, auth_logout, auth_passwordreset_request, auth_passwordreset_reset
from error import InputError
from other import clear
from conftest import user_a, user_b


def test_passwordreset_request_success(user_a):
    """
    Test 1 - Checking both request and reset
    """
    # Registered user_a with valid information logs out
    auth_logout(user_a["token"])

    # Request secret_code to change password - get from function instead of being emailed
    reset_code = auth_passwordreset_request("nbayoungboy@gmail.com")

    # Reset password using code
    auth_passwordreset_reset(reset_code, "youngboynba321")

    # Login using new_password should be a success (no errors for incorrect password)
    reset_check = auth_login("nbayoungboy@gmail.com", "youngboynba321")

    # Assert the user has been able to log in 
    assert reset_check == {"u_id": user_a["u_id"] , "token": user_a["token"]}

    clear()


def test_password_reset_success_2(user_a, user_b):
    """
    Test 2 - Checking that the reset code is successfully sent to the correct user
    """
    # Both registered users with valid information log out
    auth_logout(user_a["token"])
    auth_logout(user_b["token"])

    # Request secret_code to change password for user_b - get from function instead of being emailed
    reset_code = auth_passwordreset_request("jerrychan@gmail.com")

    # Reset password using code
    auth_passwordreset_reset(reset_code, "w89rfh@fk69")

    # Login using new_password should be a success (no errors for incorrect password)
    reset_check = auth_login("jerrychan@gmail.com", "w89rfh@fk69")

    # Assert the user has been able to log in
    assert reset_check == {"u_id": user_b["u_id"], "token": user_b["token"]}

    clear()


def test_password_reset_invalid_code_1():
    """
    Test 2.1 - Invalid reset code
    """
    reset_code = '1234567890qwertyuiopasdfghjklzxcvbnm'
    # Attempt to reset password
    with pytest.raises(InputError, match=r"Invalid password reset code"):
        auth_passwordreset_reset(reset_code, "Inv@lidresetcode")

    clear()


def test_password_reset_invalid_code_2():
    """
    Test 2.2 - InputError - Invalid reset code
    """
    reset_code = ''
    # Attempt to reset password
    with pytest.raises(InputError, match=r"Invalid password reset code"):
        auth_passwordreset_reset(reset_code, "Inv@lidresetcode")

    clear()


def test_password_reset_invalid_password(user_b):
    """
    Test 3 - InputError - Invalid password - too short
    """
    # Logout using users valid token
    auth_logout(user_b["token"])
    
    # Request secret_code to change password 
    reset_code = auth_passwordreset_request("jerrychan@gmail.com")

    # Reset password (invalid too short)
    with pytest.raises(InputError, match=r"Invalid password; too little characters"):
        auth_passwordreset_reset(reset_code, "123")

    clear()
