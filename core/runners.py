import pymongo
import argparse
from simtools.timezone import system_now

from .base import BaseSuite
from .decorators import authorize

from simtools.executable import make_this_loadable
make_this_loadable()

parser = argparse.ArgumentParser(description='Testing Parameters.')
parser.add_argument('--runner', dest="runner", type=str,
                    choices=["trash", "keep"],
                    help='Test Runner to be Used.')

cli_args = parser.parse_args()

class RunnerBase(BaseSuite):
    @classmethod
    def prepare(cls, func):
        if not isinstance(cls.storage, dict):
            print "Preparing Runner. This should not be called again."
            cls.storage = {}
            if callable(func):
                func(cls)

    def __init__(self, *args, **kwargs):
        def first_init(cls):
            runner = cli_args.runner or getattr(self, "__runner__", None)
            if runner == "trash":
                setattr(cls, "setUpClass", cls.createSiminar)
                setattr(cls, "tearDownClass", cls.deleteSiminar)

            elif runner == "keep":
                setattr(cls, "setUpClass", cls.createSiminar)

            else:
                raise Exception("Unspecified Runner. Check -h for usage")

        self.prepare(first_init)
        super(RunnerBase, self).__init__(*args, **kwargs)

class Dynamic(RunnerBase):
    __runner__ = "dynamic"

class Trash(RunnerBase):
    __runner__ = "trash"

#class Reuse(RunnerBase):
#    __runner__ = "reuse"

class Keep(RunnerBase):
    __runner__ = "keep"
