"""
server

Framework for server than runs the backend
for Flockr
"""


import sys
import smtplib, ssl
from json import dumps
from flask import Flask, request, send_from_directory
#from email.mime.multipart import MIMEMultipart
#from email.mime.text import MIMEText
#Currently unavailable
# from flask_mail import Mail, Message
from flask_cors import CORS
from auth import (
    auth_register,
    auth_login,
    auth_logout,
    auth_passwordreset_request,
    auth_passwordreset_reset
)
from channel import (
    channel_invite,
    channel_join,
    channel_leave,
    channel_addowner,
    channel_removeowner,
    channel_removemember,
    channel_details,
    channel_messages,
)
from channels import channels_create, channels_list, channels_listall
from error import InputError
from message import (
    message_send,
    message_remove,
    message_edit,
    message_sendlater,
    message_react,
    message_unreact,
    message_pin,
    message_unpin,
)
from other import users_all, admin_userpermission_change, search, clear
from user import (
    user_profile,
    user_profile_setname,
    user_profile_setemail,
    user_profile_sethandle,
    user_profile_uploadphoto,
)
from standup import (
    standup_active,
    standup_send,
    standup_start,
)


def default_handler(err):
    """
    Flask route for default handler function
    """
    response = err.get_response()
    print("response", err, err.get_response())
    response.data = dumps(
        {
            "code": err.code,
            "name": "System Error",
            "message": err.get_description(),
        }
    )
    response.content_type = "application/json"
    return response


APP = Flask(__name__, static_url_path='/src/static/')
CORS(APP)

APP.config["TRAP_HTTP_EXCEPTIONS"] = True
APP.register_error_handler(Exception, default_handler)


# Example
@APP.route("/echo", methods=["GET"])
def echo():
    """
    Flask route for echo function
    """
    data = request.args.get("data")
    if data == "echo":
        raise InputError(description='Cannot echo "echo"')
    return dumps({"data": data})


####################################################################################
#                                  Auth Routes                                     #
####################################################################################


@APP.route("/auth/register", methods=["POST"])
def register():
    """
    Flask route for auth register function
    """
    info = request.get_json()
    # Call function to register
    new_user = auth_register(
        info["email"], info["password"], info["name_first"], info["name_last"]
    )
    # Return the u_id and token from auth_register function
    return dumps(new_user)


@APP.route("/auth/login", methods=["POST"])
def login():
    """
    Flask route for auth login function
    """
    # Get the information
    info = request.get_json()
    # Call login function
    login_user = auth_login(info["email"], info["password"])
    # Return the u_id and token from auth_login function
    return dumps(login_user)


@APP.route("/auth/logout", methods=["POST"])
def logout():
    """
    Flask route for auth logout function
    """
    # Get the information
    info = request.get_json()
    # Call logout function
    logout_user = auth_logout(info["token"])
    # Return the u_id and token from auth_logout function
    return dumps(logout_user)


@APP.route("/auth/passwordreset/request", methods=["POST"])
def passwordreset_request():
    """
    Flask route for auth passwordreset request function that sends an email to the users account
    """
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "grapefruit1531@gmail.com"
    receiver_email = "grapefruit1531@gmail.com"
    password =  "throwitoutthewindow"
    info = request.get_json()

    # Call function in auth to generate reset_code
    secret_code = auth_passwordreset_request(info["email"])

    message = """\

    The code to reset your password is: """
    message += secret_code

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)

    return dumps({})


@APP.route("/auth/passwordreset/reset", methods=["POST"])
def passwordreset_reset():
    """
    Flask route for auth passwordreset reset function
    """
    info = request.get_json()
    reset = auth_passwordreset_reset(info["reset_code"], info["new_password"])

    # Return the u_id and token from auth_register function
    return dumps(reset)




####################################################################################
#                               Channel Routes                                     #
####################################################################################


@APP.route("/channel/invite", methods=["POST"])
def invite():
    """
    Flask route for channel invite function
    """
    # Request channel_invite details
    payload = request.get_json()
    token = payload["token"]
    c_id = int(payload["channel_id"])
    u_id = int(payload["u_id"])

    # Call channel invite function and return json for it
    return dumps(channel_invite(token, c_id, u_id))


@APP.route("/channel/join", methods=["POST"])
def join():
    """
    Flask route for channel join function
    """
    # Request channel_join details
    payload = request.get_json()
    token = payload["token"]
    c_id = int(payload["channel_id"])

    # Call channel join function and return json for it
    return dumps(channel_join(token, c_id))


@APP.route("/channel/leave", methods=["POST"])
def leave():
    """
    Flask route for channel leave function
    """
    # Request channel_leave details
    payload = request.get_json()
    token = payload["token"]
    c_id = int(payload["channel_id"])

    # Call channel leave function and return json for it
    return dumps(channel_leave(token, c_id))


@APP.route("/channel/addowner", methods=["POST"])
def addowner():
    """
    Flask route for channel addowner function
    """
    # Request channel_addowner details
    payload = request.get_json()
    token = payload["token"]
    c_id = int(payload["channel_id"])
    u_id = int(payload["u_id"])

    # Call channel addowner function and return json for it
    return dumps(channel_addowner(token, c_id, u_id))


@APP.route("/channel/removeowner", methods=["POST"])
def removeowner():
    """
    Flask route for channel removeowner function
    """
    # Request channel_removeowner details
    payload = request.get_json()
    token = payload["token"]
    c_id = int(payload["channel_id"])
    u_id = int(payload["u_id"])

    # Call channel removeowner function and return json for it
    return dumps(channel_removeowner(token, c_id, u_id))


@APP.route("/channel/removemember", methods=["POST"])
def removemember():
    """
    Flask route for channel removemember function
    """
    # Request channel_removemember details
    payload = request.get_json()
    token = payload["token"]
    c_id = int(payload["channel_id"])
    u_id = int(payload["u_id"])

    # Call channel removemember function and return json for it
    return dumps(channel_removemember(token, c_id, u_id))


@APP.route("/channel/details", methods=["GET"])
def details():
    """
    Flask route for channel details function
    """
    # Request channel_details details
    token = request.args.get("token")
    c_id = int(request.args.get("channel_id"))

    # Call channel details function and return json for it
    return dumps(channel_details(token, c_id))


@APP.route("/channel/messages", methods=["GET"])
def messages():
    """
    Flask route for channel messages function
    """
    # Request channel_messages details
    token = request.args.get("token")
    c_id = int(request.args.get("channel_id"))
    start = int(request.args.get("start"))

    # Call channel messages function and return json for it
    return dumps(channel_messages(token, c_id, start))


####################################################################################
#                              Channels Routes                                     #
####################################################################################


@APP.route("/channels/create", methods=["POST"])
def create_channel():
    """
    Flask route for channels create function
    """
    payload = request.get_json()
    token = payload["token"]
    name = payload["name"]
    is_public = payload["is_public"]

    # Call channels create function and return json for it
    return dumps(channels_create(token, name, is_public))


@APP.route("/channels/list", methods=["GET"])
def list_channels():
    """
    Flask route for channels list function
    """
    token = request.args.get("token")

    # Call channels create function and return json for it
    return dumps(channels_list(token))


@APP.route("/channels/listall", methods=["GET"])
def listall_channels():
    """
    Flask route for channels listall function
    """
    token = request.args.get("token")

    # Call channels listall function and return json for it
    return dumps(channels_listall(token))


####################################################################################
#                                 User Routes                                      #
####################################################################################


@APP.route("/user/profile", methods=["GET"])
def profile():
    """
    Flask route for user profile function
    """
    token = request.args.get("token")
    u_id = int(request.args.get("u_id"))

    # Call user profile function and return json for it
    return dumps(user_profile(token, u_id))


@APP.route("/user/profile/setname", methods=["PUT"])
def profile_setname():
    """
    Flask route for user profile setname function
    """
    info = request.get_json()
    token = info["token"]
    name_first = info["name_first"]
    name_last = info["name_last"]

    # Call user profile setname and return json for it
    return dumps(user_profile_setname(token, name_first, name_last))


@APP.route("/user/profile/setemail", methods=["PUT"])
def profile_setemail():
    """
    Flask route for user profile setemail function
    """
    info = request.get_json()
    token = info["token"]
    email = info["email"]

    # Call user profile setemail and return json for it
    return dumps(user_profile_setemail(token, email))


@APP.route("/user/profile/sethandle", methods=["PUT"])
def profile_sethandle():
    """
    Flask route for user profile sethandle function
    """
    info = request.get_json()
    token = info["token"]
    handle_str = info["handle_str"]

    # Call user profile sethandle and return json for it
    return dumps(user_profile_sethandle(token, handle_str))


@APP.route("/users/all", methods=["GET"])
def users_all_http():
    """
    Flask route for users all function
    """
    token = request.args.get("token")

    # Call users all and return json for it
    return dumps(users_all(token))


@APP.route("/user/profile/uploadphoto", methods=["POST"])
def user_profile_uploadphoto_http():
    """
    Flask route for users_profile uploadphoto function
    """
    info = request.get_json()
    token = info["token"]
    img_url = info["img_url"]
    x_start = int(info["x_start"])
    y_start = int(info["y_start"])
    x_end = int(info["x_end"])
    y_end = int(info["y_end"])

    # Call user_profile_uploadphoto and return json for it
    return dumps(user_profile_uploadphoto(token, img_url, x_start, y_start, x_end, y_end))


@APP.route("/src/static/<path:path>")
def send_img(path):
    """
    Flask route to display image from static url
    """
    return send_from_directory('', path)


####################################################################################
#                               Message Routes                                     #
####################################################################################


@APP.route("/message/send", methods=["POST"])
def msg_send():
    """
    Flask route for message send function
    """
    payload = request.get_json()
    token = payload["token"]
    c_id = int(payload["channel_id"])
    message = payload["message"]

    # Call message send and return json for it
    return dumps(message_send(token, c_id, message))


@APP.route("/message/remove", methods=["DELETE"])
def msg_delete():
    """
    Flask route for message remove function
    """
    payload = request.get_json()
    token = payload["token"]
    m_id = int(payload["message_id"])

    # Call message remove and return json for it
    return dumps(message_remove(token, m_id))


@APP.route("/message/edit", methods=["PUT"])
def msg_edit():
    """
    Flask route for message edit function
    """
    payload = request.get_json()
    token = payload["token"]
    m_id = int(payload["message_id"])
    message = payload["message"]

    # Call message edit and return json for it
    return dumps(message_edit(token, m_id, message))


@APP.route("/message/sendlater", methods=["POST"])
def msg_sendlater():
    """
    Flask route for message sendlater function
    """
    payload = request.get_json()
    token = payload["token"]
    c_id = int(payload["channel_id"])
    message = payload["message"]
    time_sent = int(payload["time_sent"])

    # Call message sendlater and return json for it
    return dumps(message_sendlater(token, c_id, message, time_sent))


@APP.route("/message/react", methods=["POST"])
def msg_react():
    """
    Flask route for message react function
    """
    payload = request.get_json()
    token = payload["token"]
    m_id = int(payload["message_id"])
    react_id = int(payload["react_id"])

    # Call message react and return json for it
    return dumps(message_react(token, m_id, react_id))


@APP.route("/message/unreact", methods=["POST"])
def msg_unreact():
    """
    Flask route for message unreact function
    """
    payload = request.get_json()
    token = payload["token"]
    m_id = int(payload["message_id"])
    react_id = int(payload["react_id"])

    # Call message unreact and return json for it
    return dumps(message_unreact(token, m_id, react_id))


@APP.route("/message/pin", methods=["POST"])
def msg_pin():
    """
    Flask route for message pin function
    """
    payload = request.get_json()
    token = payload["token"]
    m_id = int(payload["message_id"])

    # Call message pin and return json for it
    return dumps(message_pin(token, m_id))


@APP.route("/message/unpin", methods=["POST"])
def msg_unpin():
    """
    Flask route for message unpin function
    """
    payload = request.get_json()
    token = payload["token"]
    m_id = int(payload["message_id"])

    # Call message pin and return json for it
    return dumps(message_unpin(token, m_id))


####################################################################################
#                               Standup Routes                                     #
####################################################################################


@APP.route("/standup/active", methods=["GET"])
def active_standup():
    """
    Flask route for standup active function
    """
    token = request.args.get("token")
    c_id = int(request.args.get("channel_id"))

    # Call standup active and return json for it
    return dumps(standup_active(token, c_id))

@APP.route("/standup/start", methods=["POST"])
def start_standup():
    """
    Flask route for standup start function
    """
    payload = request.get_json()
    token = payload["token"]
    c_id = int(payload["channel_id"])
    length = int(payload["length"])

    # Call standup start and return json for it
    return dumps(standup_start(token, c_id, length))

@APP.route("/standup/send", methods=["POST"])
def send_standup():
    """
    Flask route for standup send function
    """
    payload = request.get_json()
    token = payload["token"]
    c_id = int(payload["channel_id"])
    message = payload["message"]

    # Call standup start and return json for it
    return dumps(standup_send(token, c_id, message))


####################################################################################
#                                 Other Routes                                     #
####################################################################################


@APP.route("/admin/userpermission/change", methods=["POST"])
def admin_permission_change():
    """
    Flask route for admin userpermission change function
    """
    # Request admin_userpermission_change details
    payload = request.get_json()
    token = payload["token"]
    u_id = int(payload["u_id"])
    permission_id = int(payload["permission_id"])

    # Call admin_userpermission_change function and return json for it
    return dumps(admin_userpermission_change(token, u_id, permission_id))


@APP.route("/search", methods=["GET"])
def searches():
    """
    Flask route for search function
    """
    # Request search details
    token = request.args.get("token")
    query_str = str(request.args.get("query_str"))

    # Call search function and return json for it
    return dumps(search(token, query_str))


@APP.route("/clear", methods=["DELETE"])
def http_clear():
    """
    Flask route for clear function
    """
    # Call clear function to erase all stored data
    return dumps(clear())


if __name__ == "__main__":
    APP.run(port=0)  # Do not edit this port
