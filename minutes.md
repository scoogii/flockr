# Record of Meetings - Thu09 Grape Team 3

## Monday 21 Sep

Time : 2pm-4pm (2hrs)

Learnt a bit of python together, and discussed the possible
approaches to the project (assigning roles, which data structures to use, etc).

## Tuesday 22 Sep

Time : 8pm-8:30pm (30mins)

Quick check-up on the progress of all group members regarding writing their
test files.

## Wednesday 23 Sep

Time : 9:30pm-10:30pm (1hr)

Worked on assumptions file using Google Docs. A markdown file will be made from
the document we all worked on.

## Sunday 27 Sep

Time : 3pm-4pm (1hr)

Peer reviewed test functions and discussed what needed to be fixed.

## Monday 28 Sep

Time : 2pm-4pm (2hrs)

Discussed the changes made to the test functions and also planning on how
to write and implement `auth.py`, `channel.py`, and `channels.py`.

## Tuesday 29 Sep

Time : 8:30pm - 9pm (30mins)

Updates on progress regarding functions and implementing
pytest fixtures.

## Wednesday 30 Sep

Time : 9pm - 9:15pm (15mins)

Quick check-up on progress regarding basic functionality and
implementation of functions.

## Friday 2nd October

Time : 1pm - 6pm (5hrs)

Pair/group programming - debugging of tests and functions. Simplifying Input/AccessError
messages.

## Saturday 3rd October

Time : 1:45pm - 2:15pm (30mins)

Deciding on commenting style - numbering tests for consistency, adding header
comments, double line spacing

Time : 8:45pm - 9:30pm (45mins)

Asynchronous meeting - final review of code, updating and discussion of assumptions,
and merging into master.

## Wednesday 7th October

Time : 6pm - 8pm (4hrs)

Asynchronous meeting about making files `pylint` compliant and ensuring coverage
is essentially 100% for all files.

Time : 9pm - 9:20pm

Quick group call to check-up on the progress of fixing files and tests to
maximise converage and to ensure the `pylint` pipeline passes. A merge of all
the changed files to the master branch was also discussed which will occur later.

## Monday 12th Octover

Time : 2pm - 4pm (2hrs)

Discussion about Iteration 2 - updated each other on the progress so far regarding
finishing Iteration 2 functions, code review, and planning about the future
transition of moving from dictionaries to classes.

Progress :

* Completed a first/second draft of all the Iteration 2 functions/features including
  passing pytests. Made most files pylint compliant

Assignments :

* Alan: Refining search and permission ID functions
* Christian & Eddy: Refining messages functions and tests
* Jasmin & Tony: Refining user functions and tests

## Friday 16th October

Time : 9pm - 9:30pm

Quick meeting discussing how to implement HTTP wrap-around for the Iteration 1
and 2 functions.

Progress :

* Completed all assignments from the previous meeting
* All Iteration 2 features implemented and working including their test files

Assignments :

* Alan: `channel.py` HTTP wrap-around for tests and implementing the
  Flask routing in `server.py`
* Christian: `channels.py` HTTP wrap-around for tests and implementing
  the Flask routing in `server.py`
* Eddy: `message.py` HTTP wrap-around for tests and implementing the
  Flask routing in `server.py`
* Jasmin & Tony: `auth.py` and `user.py` HTTP wrap-around for tests
  and implementing the Flask routing in `server.py`

## Monday 19th October

Time : 2pm - 4pm

Discussion on what has been implemented for HTTP, changing approach GET requests,
checking errors with status.code.

Also checked on approach authorisation and authentication

-> Updating error codes for functions
-> Updating routes and tests with GET requests

## Tuesday 20th October

Time : 9-9:30pm

Using Advanced Rest Client to test implemented (auth) servers
Creating a group checklist (on 'Open' Taskboard) to easily see what has been completed
Assigning remaining tests and servers

Progress:
Auth, Channel, User all completed

Assignments :

* Alan: `user_permission_change` and `search` HTTP tests
  Flask routing in `server.py`
* Christian: `channels.py` HTTP wrap-around for tests and implementing
  the Flask routing in `server.py`
* Eddy: `message.py` HTTP wrap-around for tests and implementing the
  Flask routing in `server.py`
* Jasmin `clear.py`
* Tony: update `user` routes in `server.py` to return immediately

## Monday 26th October

Time : 2pm - 3pm

Quick in-call meeting about how to approach Iteration 3 and delegating
new tasks between each other.

Progress:
Starting on all the new features added in Iteration 3

Assignments :

* Alan: Responsible for the standup funtions

* Jasmin: Responsible for the newly added auth functions

* Christian, Eddy & Tony: Responsible for all of the newly added message
  functions as well as the added user feature

## Monday 2nd November

Time : 1pm - 2pm

Discussed some individual problems that have came up:

* Reviewed style and variable use in auth_password reset
* Finding an appropriate method for storing url in the server for images

Also engaged in peer code-review for the new Iteration 3 features. From this,
changes were suggested for:

* Standup -> decided the approach to storing this data would be in `data.py`'s `DATA`
  as a new key "standup"
* Revised the `make_standup` function

Assignments :

* Alan: Continue implementing standup functions and tests
* Tony: Continue implementing `user_profile_upload_photo`
* Eddy & Christian: Fixing minor `message_sendlater` issue regarding time
  inconsistencies
* Jasmin: Review `standup_start` when complete (considering adding more tests)


## Thursday 5th November
Time : 11am - 11:30am

Discussed the creation of functions for tests to reduce repetition of code

Assignments :

Removing repetition in:
* Alan: Standup tests 
* Jasmin: registering with pytest fixtures
* Christian, Eddy & Tony: Message, Channel, Channels, User Tests

Planning.md: 
* Alan - Compiling responses from elicitation
* Jasmin - Writing user stories

* **ALL**: Test features with the front end


## Monday 9th November
Time : 2pm - 2:45pm

Group testing of frontend. 
Discussing possible implementation of hangman if all tasks are complete. 

Assignments :
* Alan: Logic for hangman
* Jasmin: continue working on planning documentation 
* Christian, Eddy & Tony: Improving coverage and style

## Thursday 12th November
Time : 11am - 11:30am

Deciding on which user story to write use cases for (2, 7, 8)
Discussion on extra feature for removing members from channels. 

Assignments:
* Eddy & Christian: Extra Feature - channel_removemember
* Alan: Write remaining two use cases 
* Alan, Tony & Jasmin: Validation and Interface Table

* **ALL**: State Diagrams, Read through and edit planning

