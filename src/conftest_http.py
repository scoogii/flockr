import pytest
import requests
from echo_http_test import url


@pytest.fixture
def user_a(url):
    """
    Fixture that gives us user_a's u_id and token to use
    """
    user_a_info = {
        "email": "nbayoungboy@gmail.com",
        "password": "youngboynba123",
        "name_first": "Kentrell",
        "name_last": "Gaulden"
    }

    payload = requests.post(f"{url}/auth/register", json=user_a_info)

    return payload.json()


@pytest.fixture
def user_b(url):
    """
    Fixture that gives us user_b's u_id and token to use
    """
    user_b_info = {
        "email": "jerrychan@gmail.com",
        "password": "w89rfh@fk",
        "name_first": "Jerry",
        "name_last": "Chan"
    }

    payload = requests.post(f"{url}/auth/register", json=user_b_info)

    return payload.json()


@pytest.fixture
def user_c(url):
    """
    Fixture that gives us user_c's u_id and token to use
    """
    user_c_info = {
        "email": "jamalmurray27@gmail.com",
        "password": "NuggetsInFive41",
        "name_first": "Jamal",
        "name_last": "Murray"
    }

    payload = requests.post(f"{url}/auth/register", json=user_c_info)

    return payload.json()
