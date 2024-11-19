"""
channel_messages_http_test

Testing that channel_messages works with
http implementation
"""


import requests
from echo_http_test import url
from conftest_http import user_a, user_b
from http_channel_functions import http_channel_messages, http_channel_join
from http_channels_functions import http_channels_create
from http_message_functions import http_message_send, http_message_remove, http_message_edit


def test_channel_message_http_success(url, user_a):
    """
    Test 1 - Testing that messages are successfully sent by the user
    """
    # User_a makes a channel
    channel_1 = http_channels_create(url, user_a["token"], "billionaire records", True).json()
    c_id_1 = channel_1["channel_id"]

    # User_a sends a message to the channel
    msg_1 = http_message_send(url, user_a["token"], c_id_1, "Throw it out the window").json()
    m_id_1 = msg_1["message_id"]

    # Check that the message is in the channel
    channel_msgs = http_channel_messages(url, user_a["token"], c_id_1, 0)

    result = channel_msgs.json()
    assert result == {
        "messages": [
            {
                "message_id": m_id_1,
                "u_id": user_a["u_id"],
                "message": "Throw it out the window",
                "time_created": result["messages"][0]["time_created"],
                "reacts": [
                    {
                        "react_id": 1,
                        "u_ids": [],
                        "is_this_user_reacted": False,
                    }
                ],
                "is_pinned": False,
            }
        ],
        "start": 0,
        "end": -1,
    }


def test_channel_message_http_success_50(url, user_a):
    """
    Test 2 - Testing that messages are retrieved correctly for over 50 messages
    """
    # User_a makes a channel
    channel_1 = http_channels_create(url, user_a["token"], "billionaire records", True).json()
    c_id_1 = channel_1["channel_id"]

    # Send over 50 messages to the channel (51 messages)
    message_list = []
    for i in range(0, 51):
        msg = http_message_send(url, user_a["token"], c_id_1, str(i)).json()
        m_id = msg["message_id"]

        # Use search request to find the time_created for message sent
        message_search_info = {
            "token": user_a["token"],
            "query_str": str(i),
        }

        messages = requests.get(f"{url}/search", params=message_search_info).json()
        time_sent = messages["messages"][0]["time_created"]

        message_dict = {
            "message_id": m_id,
            "u_id": user_a["u_id"],
            "message": str(i),
            "time_created": time_sent,
            "reacts": [
                {
                    "react_id": 1,
                    "u_ids": [],
                    "is_this_user_reacted": False,
                }
            ],
            "is_pinned": False,
        }
        message_list.insert(0, message_dict)

    # Remove the last message from the list because channel_messages only returns
    # 50 messages from the channel
    message_list.pop(0)

    # Check that the message is in the channel
    channel_msgs = http_channel_messages(url, user_a["token"], c_id_1, 0)

    result = channel_msgs.json()
    assert result == {
        "messages": message_list,
        "start": 0,
        "end": 50,
    }


def test_channel_message_http_invalid_channel(url, user_a, user_b):
    """
    Test 3 - System Error - for invalid channel ID
    """
    # User_a makes a channel
    channel_1 = http_channels_create(url, user_a["token"], "billionaire records", True).json()
    c_id_1 = channel_1["channel_id"]

    # User_b joins the channel
    http_channel_join(url, user_b["token"], c_id_1)

    # Check that the message is in the channel
    invalid_cid = 4566343
    payload = http_channel_messages(url, user_a["token"], invalid_cid, 0)

    assert payload.status_code == 400


def test_channel_message_http_unauth_channel(url, user_a, user_b):
    """
    Test 4 - System Error - for when the user is not part of the channel
    """
    # User_a makes a channel
    channel_1 = http_channels_create(url, user_a["token"], "billionaire records", True).json()
    c_id_1 = channel_1["channel_id"]

    # User_b cannot check channel messages because the user is not part of the channel
    payload = http_channel_messages(url, user_b["token"], c_id_1, 0)

    assert payload.status_code == 400


def test_channel_message_http_greater(url, user_a):
    """
    Test 5 - System Error - for when the selection of messages do not exist
    """
    # User_a makes a channel
    channel_1 = http_channels_create(url, user_a["token"], "billionaire records", True).json()
    c_id_1 = channel_1["channel_id"]

    # User_a cannot check channel messages because the start exceeds the number of messages
    payload = http_channel_messages(url, user_a["token"], c_id_1, 60)

    assert payload.status_code == 400
