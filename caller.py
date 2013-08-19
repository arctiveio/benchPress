from functools import partial
from simtools.uhttpclient import BlockingHTTPClient

def authtoken(func):
    def inner(self, *args, **kwargs):
        if not self.data.get("authtoken"):
            ret = Api.call(
                self.urls["authtoken"],
                data={"email": self.email, "password": self.password},
                method="POST")
            self.data.update(ret)
        func(self, *args, **kwargs)
    return inner

class Api(object):
    urls = None
    conn = BlockingHTTPClient("/tmp/api.sock")

    @classmethod
    def callback(cls, ret, callback=None):
        if ret.get("error"):
            raise Exception(ret["message"])

        data = (ret.get("data") or {}).get("data")
        if callable(callback):
            return callback(data)
        else:
            return data

    @classmethod
    def call(cls, url, data=None, method=None, callback=None):
        method = method or "get"
        if not isinstance(data, dict):
            data = {}

        if not data.get("apitoken"):
            data["apitoken"] =  "2"

        if callable(callback):
            _cb = partial(cls.callback, callback=callback)
            return cls.conn(url, callback=_cb, data=data, method=method)
        else:
            ret = cls.conn(url, callback=None, data=data, method=method)
            return cls.callback(ret)

    @classmethod
    def get_urls(cls):
        if not cls.urls:
            ret = cls.call("/urls", data={"apitoken":2})
            cls.urls = ret.get("urls")
        return cls.urls
