"""
data.py
data storage for runtime persistence
for all functions
"""

global DATA
DATA = {
    "users": [],
    "channels": [],
    "message_log": {
        "messages": [],
        "msg_counter": 1,
    },
    "standup": [],
}

"""
standup temp for storing the standup msgs
"""
#global STANDUP
#standup = []
