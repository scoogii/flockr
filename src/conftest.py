"""
Pytest fixtures thar register users
"""


import pytest
from auth import auth_register


@pytest.fixture
def user_a():
    """
    Fixture that gives us user_a's u_id and token to use
    """
    # Register a user
    user_a = auth_register("nbayoungboy@gmail.com", "youngboynba123", "Kentrell", "Gaulden")

    return {
        "u_id": user_a["u_id"],
        "token": user_a["token"],
        "name_first": "Kentrell",
        "name_last": "Gaulden",
    }


@pytest.fixture
def user_b():
    """
    Fixture that gives us user_a's u_id and token to use
    """
    # Register a user
    user_b = auth_register("jerrychan@gmail.com", "w89rfh@fk", "Jerry", "Chan")

    return {
        "u_id": user_b["u_id"],
        "token": user_b["token"],
        "name_first": "Jerry",
        "name_last": "Chan",
    }


@pytest.fixture
def user_c():
    """
    Fixture that gives us user_c's u_id and token to use
    """
    # Register a user
    user_c = auth_register("jamalmurray27@gmail.com", "NuggetsInFive41", "Jamal", "Murray")

    return {
        "u_id": user_c["u_id"],
        "token": user_c["token"],
        "name_first": "Jamal",
        "name_last": "Murray",
    }

@pytest.fixture
def user_d():
    """
    Fixture that gives us user_d's u_id and token to use
    """
    # Register a user
    user_d = auth_register("jeffsmithiscool@gmail.com", "smithjeff", "Jeff", "Smith")

    return {
        "u_id": user_d["u_id"],
        "token": user_d["token"],
        "name_first": "Jeff",
        "name_last": "Smith",
    }


@pytest.fixture
def user_e():
    """
    Fixture that gives us user_e's u_id and token to use
    """
    # Register a user
    user_e = auth_register("bobbyjones@gmail.com", "iliketoysandstuff", "Bobby", "Jones")

    return {
        "u_id": user_e["u_id"],
        "token": user_e["token"],
        "name_first": "Bobby",
        "name_last": "Jones",
    }
