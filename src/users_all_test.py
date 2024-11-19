"""
users_all

Parameters:
    token (str)
Returns:
    { users }

Description: Returns a list of all users and their associated details
"""


import pytest
from auth import auth_register
from error import AccessError
from other import users_all, clear


def test_success():
    """
    Test 1 - Success case
    """
    user_a = auth_register('nbayoungboy@gmail.com', 'youngboynba123', 'Kentrell', 'Gaulden')
    auth_register('jerrychan@gmail.com', 'w89rfh@fk', 'Jerry', 'Chan')
    auth_register('jamalmurray27@gmail.com', 'NuggetsInFive41', 'Jamal', 'Murray')


    assert users_all(user_a["token"]) == {
        'users': [
            {
                'u_id': 1,
                'email': 'nbayoungboy@gmail.com',
                'name_first': 'Kentrell',
                'name_last': 'Gaulden',
                'handle_str': 'kentrellgaulden',
                'profile_img_url': None,
            },
            {
                'u_id': 2,
                'email': 'jerrychan@gmail.com',
                'name_first': 'Jerry',
                'name_last': 'Chan',
                'handle_str': 'jerrychan',
                'profile_img_url': None,
            },
            {
                'u_id': 3,
                'email': 'jamalmurray27@gmail.com',
                'name_first': 'Jamal',
                'name_last': 'Murray',
                'handle_str': 'jamalmurray',
                'profile_img_url': None,
            }
        ],
    }

    clear()


def test_no_users():
    """
    Test 2 - AccessError - No users registered
    """
    with pytest.raises(AccessError, match=r"Invalid Token"):
        users_all('')

    clear()


def test_invalid_token():
    """
    Test 3 - AccessError - Invalid Token
    """
    auth_register('nbayoungboy@gmail.com', 'youngboynba123', 'Kentrell', 'Gaulden')
    auth_register('jerrychan@gmail.com', 'w89rfh@fk', 'Jerry', 'Chan')
    auth_register('jamalmurray27@gmail.com', 'NuggetsInFive41', 'Jamal', 'Murray')

    with pytest.raises(AccessError, match=r"Invalid Token"):
        users_all('324324323')
        