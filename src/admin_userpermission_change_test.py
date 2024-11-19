"""
admin_userpermission_change

Takes in parameters `token`, `u_id`, `permission_id`
Returns empty dictionary {}

Description: Given a User by their user ID, set their
permissions to new permissions described by permission_id

Exceptions:
 - InputError - should occur when u_id does not refer to a
                valid user
              - permission_id does not refer to a value permission
- AccessError - authorised user is not an owner
"""


import pytest
from channel import channel_join, channel_details, channel_addowner, channel_removeowner
from channels import channels_create
from error import InputError, AccessError
from other import admin_userpermission_change, clear
from conftest import user_a, user_b, user_c


def test_admin_userpermission_change_success_with_channel(user_a, user_b, user_c):
    """
    Test 1 - Member that becomes admin can add another user as a channel owner
    """
    # Create a channel and add user_b, user_c
    channel_1 = channels_create(user_a["token"], "billionaire records", True)
    c_id_1 = channel_1["channel_id"]

    # User_b and user_c joins the channel
    channel_join(user_b["token"], channel_1["channel_id"])
    channel_join(user_c["token"], channel_1["channel_id"])

    # User_a who is an admin (1) can change user_b from a member (2) to admin (1)
    admin_userpermission_change(user_a["token"], user_b["u_id"], 1)

    # User_b should be allowed to make user_c a channel_owner
    channel_addowner(user_b["token"], c_id_1, user_c["u_id"])

    # User_c should now be an owner member
    assert channel_details(user_a["token"], c_id_1) == {
        "name": "billionaire records",
        "owner_members": [
            {
                "u_id": user_a["u_id"],
                "name_first": user_a["name_first"],
                "name_last": user_a["name_last"],
                'profile_img_url': None,
            },
            {
                "u_id": user_c["u_id"],
                "name_first": user_c["name_first"],
                "name_last": user_c["name_last"],
                'profile_img_url': None,
            },
        ],
        "all_members": [
            {
                "u_id": user_a["u_id"],
                "name_first": user_a["name_first"],
                "name_last": user_a["name_last"],
                'profile_img_url': None,
            },
            {
                "u_id": user_b["u_id"],
                "name_first": user_b["name_first"],
                "name_last": user_b["name_last"],
                'profile_img_url': None,
            },
            {
                "u_id": user_c["u_id"],
                "name_first": user_c["name_first"],
                "name_last": user_c["name_last"],
                'profile_img_url': None,
            },
        ],
    }

    clear()


def test_admin_userpermission_change_success_back_to_member(user_a, user_b, user_c):
    """
    Test 2 - AccessError - tests that user that is no longer admin does not have
                           channel owner rights
    """
    # Create a channel and add user_b, user_c
    channel_1 = channels_create(user_a["token"], "Hello", True)
    c_id_1 = channel_1["channel_id"]

    # User_b and user_c joins the channel
    channel_join(user_b["token"], channel_1["channel_id"])
    channel_join(user_c["token"], channel_1["channel_id"])

    # User_a who is an admin (1) can change user_b from a member (2) to admin(1)
    admin_userpermission_change(user_a["token"], user_b["u_id"], 1)

    # User_b should be authorised to add user_c as a channel owner
    channel_addowner(user_b["token"], c_id_1, user_c["u_id"])

    # User_a who is an admin (1) can change user_b from admin (1) back to member (2)
    admin_userpermission_change(user_a["token"], user_b["u_id"], 2)

    # User_b attempts to remove user_c as a channel owner, but is no longer authorised
    with pytest.raises(AccessError, match=r"User is not an owner"):
        channel_removeowner(user_b["token"], c_id_1, user_c["u_id"])

    clear()


def test_admin_userpermission_change_to_member(user_a, user_b, user_c):
    """
    Test 3 - AccessError - Tests that user that is no longer admin
             cannot make another user admin
    """
    # User_a (1) makes user_b (2) an owner -> (1)
    admin_userpermission_change(user_a["token"], user_b["u_id"], 1)
    # User_b (1) makes user_a (1) a member -> (2)
    admin_userpermission_change(user_b["token"], user_a["u_id"], 2)

    # User_a (2) can no longer make user_c (2) a owner
    with pytest.raises(AccessError, match=r"User is not an admin"):
        admin_userpermission_change(user_a["token"], user_c["u_id"], 1)

    clear()


def test_admin_userpermission_change_invalid_u_id(user_a):
    """
    Test 4 - InputError - Invalid u_id
    """
    invalid_uid = 474563
    with pytest.raises(InputError, match=r"Invalid User ID"):
        admin_userpermission_change(user_a["token"], invalid_uid, 1)

    clear()


def test_admin_userpermission_change_invalid_token(user_a):
    """
    Test 5 - InputError - Invalid token passed in
    """
    invalid_token = ""
    with pytest.raises(AccessError, match=r"Invalid Token"):
        admin_userpermission_change(invalid_token, user_a["u_id"], 1)

    clear()


def test_admin_userpermission_change_invalid_p_id(user_a, user_b):
    """
    Test 6 - InputError - Invalid permission_id
    """
    invalid_pid = 4657382
    with pytest.raises(InputError, match=r"Invalid Permission ID"):
        admin_userpermission_change(user_a["token"], user_b["u_id"], invalid_pid)

    clear()
