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

class BaseSuite(unittest.TestCase):
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
            authtoken = Api.authenticate(email, password)
            setattr(self, "_authtoken", authtoken)
            x = func(self, *args, **kwargs)
            delattr(self, "_authtoken")
            return x
        return inner
    return _check
