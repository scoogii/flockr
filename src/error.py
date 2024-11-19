"""
error.py
Errors used in
the project's functions
"""


from werkzeug.exceptions import HTTPException


class AccessError(HTTPException):
    code = 400
    message = "No message specified"


class InputError(HTTPException):
    code = 400
    message = "No message specified"

