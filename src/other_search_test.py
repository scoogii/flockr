"""
search
Description:
    - Given a query string, return a collection of messages in all of the channels
      that the user has joined that match the query
Parameters:
    token (str)
    query_str (str)
Returns:
    { messages }
"""


import pytest
from auth import auth_register
from data import DATA
from message import message_send, message_react
from channels import channels_create
from other import search, clear


@pytest.fixture()
def user_a():
    """
    Fixture that gives us user_a's u_id and token to use
    """
    # Register a user
    return auth_register(
        "nbayoungboy@gmail.com", "youngboynba123", "Kentrell", "Gaulden"
    )


@pytest.fixture
def user_b():
    """
    Fixture that gives us user_b's u_id and token to use
    """
    # Register a user
    return auth_register("jerrychan@gmail.com", "w89rfh@fk", "Jerry", "Chan")


def get_time_created(m_id):
    """
    Retrieves the time_created for a message given a message_id
    """
    for message in DATA["message_log"]["messages"]:
        if m_id == message["message_id"]:
            return message["time_created"]


def test_search_success(user_a):
    """
    Test 1 - Successful query
    """
    # Create a channel and assign channel id to variable
    channel_1 = channels_create(user_a["token"], "billionaire records", True)
    c_id_1 = channel_1["channel_id"]

    # Send message
    msg_1 = message_send(user_a["token"], c_id_1, "testing message")
    m_id_1 = msg_1["message_id"]

    # Check
    assert search(user_a["token"], "testing message") == {
        "messages": [
            {
                "message_id": msg_1["message_id"],
                "u_id": user_a["u_id"],
                "message": "testing message",
                "time_created": get_time_created(m_id_1),
                "reacts": [
                    {
                        "react_id": 1,
                        "u_ids": [],
                        "is_this_user_reacted": False,
                    }
                ],
                "is_pinned": False,
            },
        ],
    }

    clear()


def test_search_success_multiple(user_a):
    """
    Test 2 - Successful query on multiple messages
    """
    # Create a channel and assign channel id to variable
    channel_1 = channels_create(user_a["token"], "billionaire records", True)
    c_id_1 = channel_1["channel_id"]

    # Send multiple messages
    msg_1 = message_send(user_a["token"], c_id_1, "testing message")
    m_id_1 = msg_1["message_id"]

    msg_2 = message_send(user_a["token"], c_id_1, "different message")
    m_id_2 = msg_2["message_id"]

    message_send(user_a["token"], c_id_1, "random")

    # Check
    assert search(user_a["token"], "message") == {
        "messages": [
            {
                "message_id": msg_1["message_id"],
                "u_id": user_a["u_id"],
                "message": "testing message",
                "time_created": get_time_created(m_id_1),
                "reacts": [
                    {
                        "react_id": 1,
                        "u_ids": [],
                        "is_this_user_reacted": False,
                    }
                ],
                "is_pinned": False,
            },
            {
                "message_id": msg_2["message_id"],
                "u_id": user_a["u_id"],
                "message": "different message",
                "time_created": get_time_created(m_id_2),
                "reacts": [
                    {
                        "react_id": 1,
                        "u_ids": [],
                        "is_this_user_reacted": False,
                    }
                ],
                "is_pinned": False,
            },
        ],
    }

    clear()


def test_search_empty(user_b):
    """
    Test 3 - Message does not exist
    """
    # Create a channel and assign channel id to variable
    channel_1 = channels_create(user_b["token"], "billionaire records", True)
    c_id_1 = channel_1["channel_id"]

    # Send message
    message_send(user_b["token"], c_id_1, "testing message")

    # Check
    assert search(user_b["token"], "message does not exist") == {
        "messages": [],
    }

    clear()


def test_search_repeat(user_b):
    """
    Test 4 - querying repeated messages
    """
    # Create a channel and assign channel id to variable
    channel_1 = channels_create(user_b["token"], "billionaire records", True)
    c_id_1 = channel_1["channel_id"]

    # Send repeated messages
    msg_1 = message_send(user_b["token"], c_id_1, "testing message")
    m_id_1 = msg_1["message_id"]

    msg_2 = message_send(user_b["token"], c_id_1, "testing message")
    m_id_2 = msg_2["message_id"]

    msg_3 = message_send(user_b["token"], c_id_1, "testing message")
    m_id_3 = msg_3["message_id"]

    msg_4 = message_send(user_b["token"], c_id_1, "testing message")
    m_id_4 = msg_4["message_id"]

    # Check
    assert search(user_b["token"], "testing message") == {
        "messages": [
            {
                "message_id": msg_1["message_id"],
                "u_id": user_b["u_id"],
                "message": "testing message",
                "time_created": get_time_created(m_id_1),
                "reacts": [
                    {
                        "react_id": 1,
                        "u_ids": [],
                        "is_this_user_reacted": False,
                    }
                ],
                "is_pinned": False,
            },
            {
                "message_id": msg_2["message_id"],
                "u_id": user_b["u_id"],
                "message": "testing message",
                "time_created": get_time_created(m_id_2),
                "reacts": [
                    {
                        "react_id": 1,
                        "u_ids": [],
                        "is_this_user_reacted": False,
                    }
                ],
                "is_pinned": False,
            },
            {
                "message_id": msg_3["message_id"],
                "u_id": user_b["u_id"],
                "message": "testing message",
                "time_created": get_time_created(m_id_3),
                "reacts": [
                    {
                        "react_id": 1,
                        "u_ids": [],
                        "is_this_user_reacted": False,
                    }
                ],
                "is_pinned": False,
            },
            {
                "message_id": msg_4["message_id"],
                "u_id": user_b["u_id"],
                "message": "testing message",
                "time_created": get_time_created(m_id_4),
                "reacts": [
                    {
                        "react_id": 1,
                        "u_ids": [],
                        "is_this_user_reacted": False,
                    }
                ],
                "is_pinned": False,
            },
        ],
    }

    clear()


def test_search_success_react(user_a):
    """
    Test 5 - Successful query with correct is_this_user_reacted field
    """
    # Create a channel and assign channel id to variable
    channel_1 = channels_create(user_a["token"], "billionaire records", True)
    c_id_1 = channel_1["channel_id"]

    # Send message
    msg_1 = message_send(user_a["token"], c_id_1, "testing message")
    m_id_1 = msg_1["message_id"]

    # React to the message
    message_react(user_a["token"], m_id_1, 1)

    # Check
    assert search(user_a["token"], "testing message") == {
        "messages": [
            {
                "message_id": msg_1["message_id"],
                "u_id": user_a["u_id"],
                "message": "testing message",
                "time_created": get_time_created(m_id_1),
                "reacts": [
                    {
                        "react_id": 1,
                        "u_ids": [user_a["u_id"]],
                        "is_this_user_reacted": True,
                    }
                ],
                "is_pinned": False,
            },
        ],
    }

    clear()
