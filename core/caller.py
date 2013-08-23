from functools import partial
from simtools.school import make_url
from simtools.uhttpclient import BlockingHTTPClient

class Api(object):
    urls = None
    conn = BlockingHTTPClient("/tmp/api.sock")

    @classmethod
    def authenticate(cls, email, password):
        cache_key = "authtoken_%s" % email
        cached_val = getattr(cls, cache_key, None)
        if not cached_val:
            ret = cls.fetch(
                cls.make_url("authtoken"),
                data={"email": email, "password": password},
                method="POST"
            )

            cached_val = ret
            setattr(cls, cache_key, ret)

        return cached_val

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
    def make_url(cls, name, get_args=None, **urlargs):
        url = cls.urls.get(name)
        if not url:
            raise Exception("Invalid URL %s" % name)

        return make_url(url % urlargs, get_args=get_args)

    @classmethod
    def fetch(cls, url, method, data=None, callback=None):
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
            ret = cls.fetch("/urls", method="GET", data={"apitoken":2})
            cls.urls = ret.get("urls")
        return cls.urls

Api.get_urls()
