# **Assumptions**

* ## **Data Types**

* *Email:*
    * Must have an '@' 
    * Must have a valid domain
    * Must have a string before and after '@'
    * Are case sensitve 

* *First Name, Last Name, Password*
    * Note: Assumptions regarding these structures under authentication 

* *Handle:*
    * If user has the same name, begin numbering e.g. firstlast, firstlast01
    * If users have the same first + last name which is also greater than 20 characters - string consists of 18 letters for name + 2 numbers at the end
    * Numbering begins at 01-99

* *`u_id`:*
    * Generated once a user registers and is unique
    * Begins at 1

* *Token:*
    * Tokens are unique to a user - same as `u_id` but in string format
    * Begin at 1

* *Channel_id:*
    * Easy to find
    * In a logical and linear order

* *Time_finish:*
    * Integer 
    * Must represent actual time

* *Message:*
    * Message is less than 1000 characters
    * Cannot contain emojis (for now)

* *Message_id:*
    * Each message_id is unique
    * Begin at 1

* ## **Authentication**

* *auth_login(email, password):*
    * Token returned will be the user's `u_id` in string format
    * A user can login multiple times and will be returned the same `u_id`, token

* *auth_logout(token):*
    * User must be logged in to logout
    * Once logged out token is invalidated
    * Assume there will be input

* *auth_register(email, password, name_first, name_last):*
    * User is automatically logged in after they have registered (returned `u_id` and token)
    * First name and last name: length 1-50 characters (inclusive) 
    * Email: is case sensitive e.g. email@gmail.com is the NOT the same as EMAIL@gmail.com
    * Password: 6-50 characters (inclusive)
    * Password: are case sensitive
    * Handle: A max of 99 users will have the same first and last name -> generate the handle from firstlast01..firstlast99

* ## **Message**

* *message_send(token, channel_id, message):*
    * Message CANNOT include emojis
    * Messages are Alphanumeric and can include symbols
    * Valid channel_id
    * User is part of the channel
    * Message_id starts from 1
    * Messages only range from 1 to 1000 characters

* *message_remove(token, message_id):*
    * User making the request is inside the channel where the message is

* *message_edit(token, message_id, message):*
    * New message CANNOT contain emojis, only alphanumeric and symbol characters
    * User making the request is inside the channel where the message is
    * Message exists (valid `message_id`)
    * ONLY `time_created` is adjusted when the message is edited
    * ``u_id`` of message remains with original sender

* *message functionality assumptions
    * All message details (`message_id`, `message`, `u_id`, `time_created`) are all appended
    to the global data file
    * Only the `message_id` is appended to both the channel's messages list
    * Invalid tokens for all functions raise errors

* ## *Channel*

* *channel_invite(token, channel_id, `u_id`):*
    * Users are not inviting someone that is already in the channel

* *channel_details(token, channel_id):*
    * Basic details contains the names of all the members in the channels

* *channel_messages(token, channel_id, start):*
    * The function need to be called multiple times to return the latest message if there is more than 50 messages

* *channel_leave(token, channel_id):*
    * Users cannot leave a channel that they are not in
    * If an owner leaves. they are removed from all members but are still part of owner members

* *channel_join(token, channel_id):*
    * Users cannot join a channel that they are already in

* *channel_addowner(token, channel_id, `u_id`):*
    * Users cannot add a person that is already an owner of the channel
    * Users cannot add a person that isn't a part of the channel

* *channel_removeowner(token, channel_id, `u_id`):*
    * Users cannot remove a person that is not an owner of the channel
    * Removing a user as an owner keeps them as a member still

* ## *Channels*

If an invalid token is passed in to any of the channels functions,
an `AccessError` will be raised providing a message about
how the token is invalid.

* *channels_list(token):*
    * If the logged in user is not part of any channel, `channels_list` will return an empty dictionary `{"channels": []}` with no error messages

* *channels_listall(token):*
    * Regardless of what channel(s) the user is in (private or public), `channels_listall` should list every single channel whether it is private or public

* *channels_create(token, name, is_public):*
    * Nothing should happen if a channel is created with no name (i.e. creation not successful,
      but no error messages raised)
    * All channel names are case sensitive (channel name 'Channel' is different to 'channel' for
      example)
    * Multiple channels can be created with the same name

* ## *User*

* *user_profile(token, `u_id`):*
    * Data retrieved through a valid token should already contain valid data if the 
      user has not updated any user information
    * Data recieved should already be valid and meet specification requirements

* *user_profile_setname(token, name_first, name_last):*
    * If the name is changed, original handle will remain the same (unless changed by user)
 
* *user_profile_setemail(token, email):*
    * Email is considered valid if it passes the provided function from the spec

* ## *Other* 

* *search(token, query_str):*
    * Assume there is input
    * Returns an error if there is a message that does not exist

* *users_all:*
    * The users_all will display a list of every user that is registered provided a valid token is supplied
    * Invalid tokens should return a permission error
    * The information displayed per user will be:
        * `u_id`
        * `email`
        * `name_first`
        * `name_last`
        * `handle`
