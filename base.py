import unittest
from caller import Api

def prepare(func):
    def inner(self, url, data=None, callback=None, **kwargs):
        url = Api.make_url(url, **kwargs)
        authtoken = getattr(self, "_authtoken", None)
        if authtoken:
            if not data:
                data = {}
            data["authtoken"] = authtoken
        return func(self, url, data, callback)
    return inner

from unittest.runner import TextTestResult
TextTestResult.getDescription = lambda _, test: str(test.shortDescription() or test)

class BaseSuite(unittest.TestCase):
    storage = None

    @property
    def storage(self):
        return self.__class__.storage

    def __init__(self, *args, **kwargs):
        if not isinstance(self.__class__.storage, dict):
            print "Setting Shared State Once"
            self.__class__.storage = {}

        super(BaseSuite, self).__init__(*args, **kwargs)

    @prepare
    def get(self, url, data=None, callback=None):
        return Api.fetch(url, "get", data, callback)

    @prepare
    def put(self, url, data=None, callback=None):
        return Api.fetch(url, "put", data, callback)

    @prepare
    def post(self, url, data=None, callback=None):
        return Api.fetch(url, "post", data, callback)

    @prepare
    def delete(self, url, data=None, method=None, callback=None):
        return Api.fetch(url, "delete", data, callback)

def authorize(email, password):
    def _check(func):
        def inner(self, *args, **kwargs):
            auth_val = Api.authenticate(email, password)
            setattr(self, "_authtoken", auth_val["authtoken"])
            setattr(self, "current_user_id", auth_val["user_id"])
            x = func(self, *args, **kwargs)
            delattr(self, "_authtoken")
            delattr(self, "current_user_id")
            return x
        return inner
    return _check
