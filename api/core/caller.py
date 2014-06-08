from functools import partial
from simtools.school import make_url
from simtools.uhttpclient import BlockingHTTPClient

class Api(object):
    urls = None
    conn = BlockingHTTPClient("/tmp/api.sock")

    @classmethod
    def callback(cls, ret):
        if ret.get("error"):
            raise Exception(ret["message"])

        return (ret.get("data") or {}).get("data")

    @classmethod
    def make_url(cls, name, get_args=None, **urlargs):
        url = cls.urls.get(name)
        if not url:
            raise Exception("Invalid URL %s" % name)

        return make_url(url % urlargs, get_args=get_args)

    @classmethod
    def fetch(cls, url, method, data=None):
        if not isinstance(data, dict):
            data = {}

        if not data.get("apitoken"):
            data["apitoken"] =  "2"

        ret = cls.conn(url, callback=None, data=data, method=method)
        return cls.callback(ret)

    @classmethod
    def get_urls(cls):
        if not cls.urls:
            ret = cls.fetch("/urls", method="GET", data={"apitoken":2})
            cls.urls = ret.get("urls")
        return cls.urls

Api.get_urls()
