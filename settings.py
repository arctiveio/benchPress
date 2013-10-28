STUDENT_EMAIL = ""
STUDENT_PASSWORD = ""

INSTRUCTOR_EMAIL = ""
INSTRUCTOR_PASSWORD = ""

APIHOSTS = "/tmp/api.sock"
PARTYHOST = "/tmp/party.sock"

try:
    from local_settings import *
except ImportError, e:
    print e
