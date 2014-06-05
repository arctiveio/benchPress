STUDENT_EMAIL = ""
STUDENT_PASSWORD = ""

INSTRUCTOR_EMAIL = ""
INSTRUCTOR_PASSWORD = ""

try:
    from local_settings import *
except ImportError, e:
    print e
