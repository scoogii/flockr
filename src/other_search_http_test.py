"""
search_http_test

Testing that search works with
http implementation
"""


import requests
import pytest
from echo_http_test import url
from conftest_http import user_a, user_b
from http_channels_functions import http_channels_create
from http_message_functions import http_message_send
from http_other_functions import http_search


def test_search_success(url, user_a):
    """
    Test 1 - Successful query
    """
    # User_a makes a channel
    channel_1 = http_channels_create(url, user_a["token"], "billionaire records", True).json()
    c_id_1 = channel_1["channel_id"]

    # User_a sends a message to the channel
    msg_1 = http_message_send(url, user_a["token"], c_id_1, "testing message").json()
    m_id_1 = msg_1["message_id"]

    search_results = http_search(url, user_a["token"], "testing message")

    # Check
    result = search_results.json()
    assert result == {
        "messages": [
            {
                "message_id": m_id_1,
                "u_id": user_a["u_id"],
                "message": "testing message",
                "time_created": result["messages"][0]["time_created"],
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


def test_search_success_multiple(url, user_a):
    """
    Test 2 - Successful query on multiple messages
    """
    # User_a makes a channel
    channel_1 = http_channels_create(url, user_a["token"], "billionaire records", True).json()
    c_id_1 = channel_1["channel_id"]

    # User_a sends a message to the channel
    msg_1 = http_message_send(url, user_a["token"], c_id_1, "testing message").json()
    m_id_1 = msg_1["message_id"]

    # User_a sends another message to the channel
    msg_2 = http_message_send(url, user_a["token"], c_id_1, "different message").json()
    m_id_2 = msg_2["message_id"]

    search_results = http_search(url, user_a["token"], "message")

    # Check
    result = search_results.json()
    assert result == {
        "messages": [
            {
                "message_id": m_id_1,
                "u_id": user_a["u_id"],
                "message": "testing message",
                "time_created": result["messages"][0]["time_created"],
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
                "message_id": m_id_2,
                "u_id": user_a["u_id"],
                "message": "different message",
                "time_created": result["messages"][1]["time_created"],
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


def test_search_empty(url, user_b):
    """
    Test 3 - Message does not exist
    """
    # User_b makes a channel
    channel_1 = http_channels_create(url, user_b["token"], "billionaire records", True).json()
    c_id_1 = channel_1["channel_id"]

    # User_b sends a message to the channel
    http_message_send(url, user_b["token"], c_id_1, "testing message")

    search_results = http_search(url, user_b["token"], "message does not exist")

    # Check
    result = search_results.json()
    assert result == {
        "messages": [],
    }


def test_search_repeat(url, user_a):
    """
    Test 4 - querying repeated messages
    """
    # User_a makes a channel
    channel_1 = http_channels_create(url, user_a["token"], "billionaire records", True).json()
    c_id_1 = channel_1["channel_id"]

    # User_a sends a message to the channel
    msg_1 = http_message_send(url, user_a["token"], c_id_1, "testing message").json()
    m_id_1 = msg_1["message_id"]

    # User_a sends a message to the channel
    msg_2 = http_message_send(url, user_a["token"], c_id_1, "testing message").json()
    m_id_2 = msg_2["message_id"]

    # User_a sends a message to the channel
    msg_3 = http_message_send(url, user_a["token"], c_id_1, "testing message").json()
    m_id_3 = msg_3["message_id"]

    # User_a sends a message to the channel
    msg_4 = http_message_send(url, user_a["token"], c_id_1, "testing message").json()
    m_id_4 = msg_4["message_id"]

    search_results = http_search(url, user_a["token"], "message")

    # Check
    result = search_results.json()
    assert result == {
        "messages": [
            {
                "message_id": m_id_1,
                "u_id": user_a["u_id"],
                "message": "testing message",
                "time_created": result["messages"][0]["time_created"],
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
                "message_id": m_id_2,
                "u_id": user_a["u_id"],
                "message": "testing message",
                "time_created": result["messages"][1]["time_created"],
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
                "message_id": m_id_3,
                "u_id": user_a["u_id"],
                "message": "testing message",
                "time_created": result["messages"][2]["time_created"],
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
                "message_id": m_id_4,
                "u_id": user_a["u_id"],
                "message": "testing message",
                "time_created": result["messages"][3]["time_created"],
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
