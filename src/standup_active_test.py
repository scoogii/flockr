"""
standup_active

Takes in (token, channel_id)
Returns { is_active, time_finish }

Description: For a given channel, return whether a standup is active in it,
and what time the standup finishes.
If no standup is active, then time_finish returns None

Exceptions:
- InputError when any of:
    - Channel ID is not a valid channel

"""


from time import sleep
import pytest
from channels import channels_create
from error import InputError, AccessError
from standup import standup_active, standup_start
from other import clear
from data import DATA
from conftest import user_a, user_b


def get_time_finish(c_id):
    """
    Helper function to get time finish
    Parameters:
        c_id (int)
    Returns:
        standup["time_finish"] (int)
    """
    for standup in DATA["standup"]:
        if c_id == standup["channel_id"]:
            return standup["time_finish"]


def test_standup_active_inactive(user_a):
    """
    Test 1 - Standup is not active
    """
    # User_a makes a channel
    channel_1 = channels_create(user_a["token"], "billionaire records", True)
    c_id_1 = channel_1["channel_id"]

    # User_a runs a standup
    status = standup_active(user_a["token"], c_id_1)

    assert status == {
        "is_active": False,
        "time_finish": None,
    }

    clear()


def test_standup_active_active(user_a):
    """
    Test 2 - Standup is active
    """
    # User_a makes a channel
    channel_1 = channels_create(user_a["token"], "billionaire records", True)
    c_id_1 = channel_1["channel_id"]

    standup_start(user_a["token"], c_id_1, 200)
    status = standup_active(user_a["token"], c_id_1)

    assert status == {
        "is_active": True,
        "time_finish": get_time_finish(c_id_1),
    }

    clear()


def test_standup_active_wait(user_a):
    """
    Test 3 - Standup wait
    """
    # User_a makes a channel
    channel_1 = channels_create(user_a["token"], "billionaire records", True)
    c_id_1 = channel_1["channel_id"]

    standup_start(user_a["token"], c_id_1, 1)
    status = standup_active(user_a["token"], c_id_1)

    assert status == {
        "is_active": True,
        "time_finish": get_time_finish(c_id_1)
    }

    # Sleep
    sleep(2)
    status = standup_active(user_a["token"], c_id_1)
    assert status == {
        "is_active": False,
        "time_finish": None
    }

    clear()


def test_standup_active_multiple_channels(user_a):
    """
    Test 4 - Checking if a standup is active for a channel
    that is not the first channel
    """
    # User_a makes a channel
    channel_1 = channels_create(user_a["token"], "billionaire records", True)
    c_id_1 = channel_1["channel_id"]

    # User_a makes another channel
    channel_2 = channels_create(user_a["token"], "the cage", True)
    c_id_2 = channel_2["channel_id"]

    # User_a starts a standup in both channels
    standup_start(user_a["token"], c_id_1, 200)
    standup_start(user_a["token"], c_id_2, 200)

    # Check if channel 2 has an active standup
    status = standup_active(user_a["token"], c_id_2)

    assert status == {
        "is_active": True,
        "time_finish": get_time_finish(c_id_2),
    }

    clear()


def test_standup_active_invalid_c_id(user_a):
    """
    Test 5 - InputError - invalid channel ID
    """
    # Error should be raised since channel_id is invalid
    invalid_c_id = 12345
    with pytest.raises(InputError):
        standup_active(user_a["token"], invalid_c_id)

    clear()


def test_standup_active_invalid_token(user_a):
    """
    Test 6 - AccessErorr - Invalid token
    """
    # User_a makes a channel
    channel_1 = channels_create(user_a["token"], "billionaire records", True)
    c_id_1 = channel_1["channel_id"]

    # Error should be raised since token passed in is invalid
    invalid_token = '12345'
    with pytest.raises(AccessError, match=r"Invalid Token"):
        standup_active(invalid_token, c_id_1)

    clear()
