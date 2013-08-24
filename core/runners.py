import argparse
from simtools.timezone import system_now

from .base import BaseSuite
from .decorators import authorize

import sys
from os.path import abspath, dirname, join
PATH = abspath(dirname(__file__))
sys.path.append(join(PATH, '..'))
import settings

parser = argparse.ArgumentParser(description='Testing Parameters.')
parser.add_argument('--runner', dest="runner", type=str,
                    choices=['trash', 'keep', 'reuse'],
                    help='Test Runner to be Used.')

parser.add_argument('--siminar_id', dest="siminar_id", type=str, nargs=1,
                    help='SiminarID to consume in test cases.')

cli_args = parser.parse_args()

class RunnerBase(BaseSuite):
    @classmethod
    def prepare(cls, func):
        if not isinstance(cls.storage, dict):
            print "Preparing Runner. This should not be called again."
            cls.storage = {}
            if callable(func):
                func(cls)

    @classmethod
    @authorize(settings.INSTRUCTOR_EMAIL, settings.INSTRUCTOR_PASSWORD)
    def createSiminar(cls):
        cls.storage["instructor_id"] = cls.current_user_id
        ret = cls.post(
            "siminars",
            data={
                "title": "Siminar Created on %s" % system_now().strftime("%c")
            })

        cls.storage["siminar_id"] = ret.get("created")
        print "Created New Siminar %s" % cls.storage["siminar_id"]

    @classmethod
    @authorize(settings.INSTRUCTOR_EMAIL, settings.INSTRUCTOR_PASSWORD)
    def deleteSiminar(self):
        if self.storage.get("siminar_id"):
            print "Erasing Siminar %s" % self.storage["siminar_id"]
            siminar_id = self.storage["siminar_id"]
            self.delete("agora_delete", data={"object_ids": [siminar_id]})

    def __init__(self, *args, **kwargs):
        def first_init(cls):
            runner = cli_args.runner or getattr(self, "__runner__", None)
            if runner == "trash":
                setattr(cls, "setUpClass", cls.createSiminar)
                setattr(cls, "tearDownClass", cls.deleteSiminar)

            elif runner == "keep":
                setattr(cls, "setUpClass", cls.createSiminar)

            elif runner == "reuse":
                if cli_args.siminar_id:
                    cls.storage["siminar_id"] = cli_args.siminar_id
                else:
                    raise Exception("Must provide --siminar_id with --runner reuse")
            else:
                raise Exception("Unspecified Runner. Check -h for usage")

        self.prepare(first_init)
        super(RunnerBase, self).__init__(*args, **kwargs)

class Dynamic(RunnerBase):
    __runner__ = "dynamic"

class Trash(RunnerBase):
    __runner__ = "trash"

class Reuse(RunnerBase):
    __runner__ = "reuse"

class Keep(RunnerBase):
    __runner__ = "keep"
