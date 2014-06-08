import unittest

from .caller import Api
from .logger import get_logger

from collections import defaultdict
from simtools.timezone import system_now
from functools import partial

from unittest.runner import TextTestResult
TextTestResult.getDescription = lambda _, test: \
        str(test.shortDescription() or test)

class BaseSuite(unittest.TestCase):
    logger = get_logger("UnitTestingLogger")
    storage = None
    current_user_id = None
    activities = defaultdict(set)

    @classmethod
    def _fetch(cls, url, method, data=None, **kwargs):
        url = Api.make_url(url, **kwargs)
        if not data:
            data = {}

        authtoken = getattr(cls, "_authtoken", None)
        if authtoken:
            data["authtoken"] = authtoken

        ret = Api.fetch(url, method, data)
        return ret


    @property
    def storage(self):
        return self.__class__.storage

    def __init__(self, *args, **kwargs):
        if not isinstance(self.__class__.storage, dict):
            self.logger.debug("Setting Shared State Once")
            self.__class__.storage = {}

        super(BaseSuite, self).__init__(*args, **kwargs)

    @classmethod
    def get(cls, url, url_args=None, data=None, **kwargs):
        return cls._fetch(url, "get", data, **kwargs)

    @classmethod
    def put(cls, url, data=None, **kwargs):
        return cls._fetch(url, "put", data, **kwargs)

    @classmethod
    def post(cls, url, data=None, **kwargs):
        ret = cls._fetch(url, "post", data, **kwargs)
        if cls.__runner__ == "trash":
            _id = ret.get("created")
            if not _id:
                cls.logger.error(
                    "%s POST call does not return {'created': <_id>}. "
                    "Cannot not cleanup on exit" % url)
            else:
                authtoken = getattr(cls, "_authtoken", None)
                cls.activities[authtoken].add(_id)

        return ret

    @classmethod
    def delete(cls, url, data=None, **kwargs):
        return cls._fetch(url, "delete", data, **kwargs)

    @classmethod
    def clear_user(cls):
        delattr(cls, "_authtoken")
        delattr(cls, "current_user_id")

    @classmethod
    def login_user(cls, email, password):
        cache_key = "authtoken_%s" % email
        cached_val = getattr(cls, cache_key, None)
        if not cached_val:
            cached_val = cls.post(
                "authtoken",
                data={"email": email, "password": password})

            setattr(cls, cache_key, cached_val)

        if cls.__runner__ == "trash":
            cls.activities[cached_val["authtoken"]].add(cached_val["authtoken"])

        setattr(cls, "_authtoken", cached_val["authtoken"])
        setattr(cls, "current_user_id", cached_val["user_id"])

    @classmethod
    def logout_user(cls, email):
        authtoken = getattr(Api, "authtoken_%s" % email, None)
        if not authtoken:
            return

        cls._authtoken = authtoken
        cls.delete("authtoken", "delete", {"authtoken": authtoken})

        cls.clear_user()
        delattr(cls, "authtoken_%s" % email)


    @classmethod
    def go_run(cls):
        suite = unittest.TestLoader().loadTestsFromTestCase(cls)
        unittest.TextTestRunner(descriptions=True, verbosity=2).run(suite)
