import unittest

from .caller import Api
from simtools.timezone import system_now

from unittest.runner import TextTestResult
TextTestResult.getDescription = lambda _, test: \
        str(test.shortDescription() or test)

def prepare(func):
    def inner(self, url, data=None, callback=None, **kwargs):
        if not isinstance(data, dict):
            data = {}

        url = Api.make_url(url, **kwargs)

        authtoken = getattr(self, "_authtoken", None)
        if authtoken:
            data["authtoken"] = authtoken

        return func(self, url, data, callback)
    return inner

class BaseSuite(unittest.TestCase):
    storage = None
    current_user_id = None

    @property
    def storage(self):
        return self.__class__.storage

    def __init__(self, *args, **kwargs):
        if not isinstance(self.__class__.storage, dict):
            print "Setting Shared State Once"
            self.__class__.storage = {}

        super(BaseSuite, self).__init__(*args, **kwargs)

    @classmethod
    @prepare
    def get(self, url, data=None, callback=None):
        return Api.fetch(url, "get", data, callback)

    @classmethod
    @prepare
    def put(self, url, data=None, callback=None):
        return Api.fetch(url, "put", data, callback)

    @classmethod
    @prepare
    def post(self, url, data=None, callback=None):
        return Api.fetch(url, "post", data, callback)

    @classmethod
    @prepare
    def delete(self, url, data=None, method=None, callback=None):
        return Api.fetch(url, "delete", data, callback)

    @classmethod
    def clear_user(cls):
        delattr(cls, "_authtoken")
        delattr(cls, "current_user_id")

    @classmethod
    def login_user(cls, email, password):
        auth_val = Api.authenticate(email, password)
        setattr(cls, "_authtoken", auth_val["authtoken"])
        setattr(cls, "current_user_id", auth_val["user_id"])

    @classmethod
    def logout_user(cls, email):
        authtoken = getattr(Api, "authtoken_%s" % email, None)
        if not authtoken:
            return

        cls._authtoken = authtoken
        cls.delete("authtoken", "delete", {"authtoken": authtoken})
        cls.clear_user()
        delattr(Api, "authtoken_%s" % email)
