import argparse
from simtools.timezone import system_now

from .base import BaseSuite

CLI = argparse.ArgumentParser(description='Testing Parameters.')
CLI.add_argument('--runner', dest="runner", type=str,
                    choices=["trash", "keep"],
                    help='Test Runner to be Used.')


class RunnerBase(BaseSuite):
    @classmethod
    def startRecording(cls):
        cls.logger.info("Recording all new activities")

    @classmethod
    def deleteFootPrint(cls):
        if not cls.activities:
            return

        cls.logger.warn(
            "Deleting all activities saved in this test run. %s" % cls.activities)

        for authtoken, _ids in cls.activities.iteritems():
            cls.delete("agora_delete",
                       {"object_ids": list(_ids), "authtoken": authtoken})


    @classmethod
    def prepare(cls, func):
        if not isinstance(cls.storage, dict):
            cls.logger.info("Preparing Runner")
            cls.storage = {}
            if callable(func):
                func(cls)

    def __init__(self, *args, **kwargs):
        self.cli_args = CLI.parse_args()

        def first_init(cls):
            runner = self.cli_args.runner or getattr(self, "__runner__", None)
            setattr(cls, "__runner__", runner)

            if runner == "trash":
                cls.logger.warn("Using Trash Runner. All new Activities will be deleted.")
                setattr(cls, "setUpClass", cls.startRecording)
                setattr(cls, "tearDownClass", cls.deleteFootPrint)

            elif runner == "keep":
                cls.logger.warn("Using Persistant Runner. Will not Delete Activities")

            else:
                raise Exception("Unspecified Runner. Check -h for usage")

        self.prepare(first_init)
        super(RunnerBase, self).__init__(*args, **kwargs)


class Trash(RunnerBase):
    __runner__ = "trash"


class Keep(RunnerBase):
    __runner__ = "keep"
