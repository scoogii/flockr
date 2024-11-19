"""
admin_userpermission_change_http_test

Testing that admin_userpermission_change works with
http implementation
"""


import pytest
import requests
from echo_http_test import url
from conftest_http import user_a, user_b, user_c
from http_channel_functions import (
    http_channel_join,
    http_channel_addowner,
    http_channel_removeowner,
    http_channel_details
)
from http_channels_functions import http_channels_create
from http_other_functions import http_admin_userpermission_change


def test_admin_userpermission_change_success_with_channel(url, user_a, user_b, user_c):
    """
    Test 1 - Admin user permission change is successful on channels
    """
    # User_a makes a channel
    channel_1 = http_channels_create(url, user_a["token"], "billionaire records", True).json()
    c_id_1 = channel_1["channel_id"]

    # User_b joins the channel
    http_channel_join(url, user_b["token"], c_id_1)

    # User_c joins the channel
    http_channel_join(url, user_c["token"], c_id_1)

    # User_a who is an admin (1) can change user_b from a member (2) to admin (1)
    http_admin_userpermission_change(url, user_a["token"], user_b["u_id"], 1)

    # User_b makes User_c the channel owner
    http_channel_addowner(url, user_b["token"], c_id_1, user_c["u_id"])

    # Get the details in which now user_a and user_c are channel_owners
    payload = http_channel_details(url, user_a["token"], c_id_1)

    result = payload.json()
    assert result == {
        "name": "billionaire records",
        "owner_members": [
            {
                "u_id": user_a["u_id"],
                "name_first": "Kentrell",
                "name_last": "Gaulden",
                'profile_img_url': None,
            },
            {
                "u_id": user_c["u_id"],
                "name_first": "Jamal",
                "name_last": "Murray",
                'profile_img_url': None,
            },
        ],
        "all_members": [
            {
                "u_id": user_a["u_id"],
                "name_first": "Kentrell",
                "name_last": "Gaulden",
                'profile_img_url': None,
            },
            {
                "u_id": user_b["u_id"],
                "name_first": "Jerry",
                "name_last": "Chan",
                'profile_img_url': None,
            },
            {
                "u_id": user_c["u_id"],
                "name_first": "Jamal",
                "name_last": "Murray",
                'profile_img_url': None,
            },
        ],
    }


def test_admin_userpermission_change_success_back_to_member(url, user_a, user_b, user_c):
    """
    Test 2 - Admin user permission change is successful on channels
    """
    # User_a makes a channel
    channel_1 = http_channels_create(url, user_a["token"], "billionaire records", True).json()
    c_id_1 = channel_1["channel_id"]

    # User_b joins the channel
    http_channel_join(url, user_b["token"], c_id_1)

    # User_c joins the channel
    http_channel_join(url, user_c["token"], c_id_1)

    # User_a who is an admin (1) can change user_b from a member (2) to admin (1)
    http_admin_userpermission_change(url, user_a["token"], user_b["u_id"], 1)

    # User_b makes User_c the channel owner
    http_channel_addowner(url, user_b["token"], c_id_1, user_c["u_id"])

    # User_a who is an admin (1) can change user_b from admin (1) back to member (2)
    http_admin_userpermission_change(url, user_a["token"], user_b["u_id"], 2)

    # User_b tries to remove user_c
    # User_b cannot remove owner based on no longer being an admin
    payload = http_channel_removeowner(url, user_b["token"], c_id_1, user_c["u_id"])

    assert payload.status_code == 400


def test_admin_userpermission_change_to_member(url, user_a, user_b, user_c):
    """
    Test 3 - AccessError - Tests that user that is no longer admin
             cannot make another user admin
    """
    # User_a (1) makes user_b (2) an owner -> (1)
    http_admin_userpermission_change(url, user_a["token"], user_b["u_id"], 1)

    # User_b (1) makes user_a (1) a member -> (2)
    http_admin_userpermission_change(url, user_b["token"], user_a["u_id"], 2)

    # User_a (2) can no longer make user_c (2) a owner
    payload = http_admin_userpermission_change(url, user_a["token"], user_c["u_id"], 1)

    assert payload.status_code == 400


def test_admin_userpermission_change_invalid_u_id(url, user_a, user_b):
    """
    Test 4 - InputError - Invalid u_id
    """
    invalid_uid = 12345
    payload = http_admin_userpermission_change(url, user_a["token"], invalid_uid, 1)
    
    assert payload.status_code == 400


def test_admin_userpermission_change_invalid_token(url, user_a, user_b):
    """
    Test 5 - InputError - Invalid token passed in
    """
    invalid_token = ""
    payload = http_admin_userpermission_change(url, invalid_token, user_b["u_id"], 1)

    assert payload.status_code == 400


def test_admin_userpermission_change_invalid_p_id(url, user_a, user_b):
    """
    Test 6 - InputError - Invalid permission_id
    """
    invalid_pid = 12345
    payload = http_admin_userpermission_change(url, user_a["token"], user_b["u_id"], invalid_pid)

    assert payload.status_code == 400
