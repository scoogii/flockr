"""
auth_register

Takes in parameters `email`, `password`, "name_first", "name_last"
Returns a dictionary {"u_id", "token"}

Description: Given a valid email,password, first & last name,
             creates an account, generates a handle and returns u_id and token

InputError should occur when:
- Email entered is not a valid email (format)
- Email entered does already belongs to another user
- Password is invalid: - less than 6 characters long - contains non-ascii characters
- name_first is invalid: not between 1-50 characters - contains non-letters (except " " and "-")
- name_last is invalid: not between 1-50 characters - contains non-letters (except " " and "-")
"""


import pytest
from auth import auth_register
from error import InputError
from user import user_profile
from other import users_all
from other import clear


def test_registered_success():
    """
    Test 1.1 - Registering a user with valid information -> returns u_id and token
    (contains later test for when user functions are implemented)
    """
    # REGISTER USER A
    user_a = auth_register("nbayoungboy@gmail.com", "youngboynba123", "Kentrell", "Gaulden")
    # get u_id and token
    u_id_1 = user_a["u_id"]
    token_1 = user_a["token"]

    # Assert user is registered and logged in by checking the return values of u_id and token
    assert user_a == {"u_id": u_id_1, "token": token_1}

    clear()


def test_register_all_():
    """
    Test 1.2 - Registering a user with valid information -> returns u_id and token
    (contains later test for when user functions are implemented)
    """
    # REGISTER USER B
    auth_register("nbayoungboy@gmail.com", "youngboynba123", "Kentrell", "Gaulden")
    user_b = auth_register("jerrychan@gmail.com", "w89rfh@fk", "Jerry", "Chan")
    # get u_id and token
    token_2 = user_b["token"]

    # Check details are added correctly
    assert users_all(token_2) == {
        "users": [
            {
                "u_id": 1,
                "email": "nbayoungboy@gmail.com",
                "name_first": "Kentrell",
                "name_last": "Gaulden",
                "handle_str": "kentrellgaulden",
                "profile_img_url": None,
            },
            {
                "u_id": 2,
                "email": "jerrychan@gmail.com",
                "name_first": "Jerry",
                "name_last": "Chan",
                "handle_str": "jerrychan",
                "profile_img_url": None,
            },
        ]
    }

    clear()


def test_registered_profile():
    """
    Test 2 - Registering a user with valid information -> returns u_id and token
    (contains later test for when user functions are implemented)
    """
    # REGISTER USER C
    user_c = auth_register("jamalmurray27@gmail.com", "NuggetsInFive41", "Jamal", "Murray")
    # get u_id and token
    u_id_3 = user_c["u_id"]
    token_3 = user_c["token"]

    # Assert user is registered by checking the return values of u_id and token
    assert user_c == {"u_id": u_id_3, "token": token_3}

    profile_c = user_profile(token_3, u_id_3)
    assert profile_c["user"]["email"] == "jamalmurray27@gmail.com"
    assert profile_c["user"]["name_first"] == "Jamal"
    assert profile_c["user"]["name_last"] == "Murray"
    assert profile_c["user"]["handle_str"] == "jamalmurray"

    clear()


def test_unique_id():
    """
    Test 3.1 - Check two users are not given the same u_id
    """
    user_d = auth_register("jeffsmith.iscool@gmail.com", "smithjeff", "Jeff", "Smith")
    user_e = auth_register("bobbyjones@gmail.com", "iliketoysandstuff", "Bobby ", "  Jones ")
    assert user_d["u_id"] != user_e["u_id"]

    clear()


def test_unique_token():
    """
    Test 3.2 Check two users are not given the same token
    """
    user_f = auth_register("noname@hotmail.com", "sjfbol23", "Name", "No")
    user_g = auth_register("user123@gmail.com", "laiyofb#cz", "User", "  One ")
    assert user_f["token"] != user_g["token"]

    clear()


def test_complex_email():
    """
    Test 4 - Check emails with longer domains register is still considered valid
    """
    user_h = auth_register("student@unsw.edu.au", "UNSW4Life", "Sally", "Smith")
    u_id_4 = user_h["u_id"]
    token_4 = user_h["token"]
    assert user_h == {"u_id": u_id_4, "token": token_4}

    clear()


def test_handle_duplicates():
    """
    Test 5.1 - Check handle numbering system
    """
    user_i = auth_register("u1@gmail.com", "password1", "Benjamin", "William-Jones")
    check_i = user_profile(user_i["token"], user_i["u_id"])
    assert check_i["user"]["handle_str"] == "benjaminwilliam-jone"
    auth_register("u2@gmail.com", "password2", "Benjamin", "William-Jones")
    auth_register("u3@gmail.com", "password3", "Benjamin", "William-Jones")
    user_j = auth_register("u4@gmail.com", "password4", "Benjamin", "William-Jones")
    check_j = user_profile(user_j["token"], user_j["u_id"])
    assert check_j["user"]["handle_str"] == "benjaminwilliam-jo03"

    clear()


def test_handle_duplicate_large():
    """
    Test 5.2 - Check handle numbering system - more than 10 of the same
    """
    auth_register("h@gmail.com", "password0", "John", "Smith")
    auth_register("h1@gmail.com", "password1", "John", "Smith")
    auth_register("h2@gmail.com", "password2", "John", "Smith")
    auth_register("h3@gmail.com", "password3", "John", "Smith")
    auth_register("h4@gmail.com", "password4", "John", "Smith")
    auth_register("h5@gmail.com", "password5", "John", "Smith")
    auth_register("h6@gmail.com", "password6", "John", "Smith")
    auth_register("h7@gmail.com", "password7", "John", "Smith")
    auth_register("h8@gmail.com", "password8", "John", "Smith")
    auth_register("h9@gmail.com", "password9", "John", "Smith")
    auth_register("h10@gmail.com", "password10", "John", "Smith")
    user_k = auth_register("h11@gmail.com", "password11", "John", "Smith")
    check_k = user_profile(user_k["token"], user_k["u_id"])
    assert check_k["user"]["handle_str"] == "johnsmith11"

    clear()


#InputError Tests

# Tests 6: Email Cases
def test_empty_email():
    """
    Test 6.1 - Empty input for email
    """
    with pytest.raises(InputError, match=r"Email is invalid"):
        auth_register("", "jjkbbjssdf", "No", "Email")


def test_invalid_email_1():
    """
    Test 6.2 - Email entered is not a valid email
    """
    with pytest.raises(InputError, match=r"Email is invalid"):
        auth_register("email.com", "abcdefg", "Alden", "Cox")
    with pytest.raises(InputError, match=r"Email is invalid"):
        auth_register("email@", "ibufowcss", "George", "Mip")


def test_used_email():
    """
    Test 6.3 - Email address is already being used by another user
    """
    with pytest.raises(InputError, match=r"Email taken by another user"):
        auth_register("usedemail@gmail.com", "mypassword", "Harry", "Jones")
        auth_register("usedemail@gmail.com", "newpassword", "Harry", "James")


# Test 7/8: Invalid Password Cases
def test_invalid_password_length_short():
    """
    Test 7.1 - Password entered is less than 6 characters long
    """
    with pytest.raises(InputError, match=r"Invalid password; too little characters"):
        auth_register("shortpassword@gmail.com", "hi", "Miranda", "Shaffer")


def test_invalid_password_length_space():
    """
    Test 7.2 - Password entered is less than 6 characters long
    """
    with pytest.raises(InputError, match=r"Invalid password; too little characters"):
        auth_register("longpassword@gmail.com", "   ", "Heidi", "Shaffer")



# Tests 8: Invalid name length - not between 1 and 50 characters in length (inclusive)
def test_invalid_first_name_short():
    """
    Test 8.1 - name_first less than one character
    """
    with pytest.raises(InputError, match=r"Name must be between 1 and 50 characters inclusive"):
        auth_register("firstnameshort@gmail.com", "secret", "", "Shaffer")


def test_invalid_first_name_long():
    """
    Test 8.2 - name_first greater than 50 characters
    """
    with pytest.raises(InputError, match=r"Name must be between 1 and 50 characters inclusive"):
        auth_register("firstnamelong@gmail.com", "a@21dska", "a"*51, "Luke")


def test_invalid_last_short():
    """
    Test 8.3 - name_last less than one character
    """
    with pytest.raises(InputError, match=r"Name must be between 1 and 50 characters inclusive"):
        auth_register("lastnameshort@gmail.com", "sgblwjb3849#", "Bill", "")


def test_invalid_last_long():
    """
    Test 8.4 - name_last greater than 50 characters
    """
    with pytest.raises(InputError, match=r"Name must be between 1 and 50 characters inclusive"):
        auth_register("lastnamelong@gmail.com", "&JSooaf", "Bob", "a"*51)
