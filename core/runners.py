import argparse
from simtools.timezone import system_now

from .base import BaseSuite
from .decorators import authorize

import sys
from os.path import abspath, dirname, join
PATH = abspath(dirname(__file__))
sys.path.append(join(PATH, '..'))
import settings

def parseSiminarId():
    parser = argparse.ArgumentParser(description='Testing Parameters.')
    parser.add_argument('--siminar_id', dest="siminar_id", type=str, nargs=1,
                        help='SiminarID to consume in test cases.')
    args = parser.parse_args()
    if not args.siminar_id:
        raise Exception("--siminar_id not found. Check -h for usage.")

class TrashSiminar(BaseSuite):
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

    @classmethod
    def setUpClass(self):
        self.createSiminar()

    @classmethod
    def tearDownClass(self):
        self.deleteSiminar()

class ExistingSiminar(BaseSuite):
    def __init__(self, *args, **kwargs):
        if not isinstance(self.__class__.storage, dict):
            print "Setting Shared State Once"
            self.__class__.storage = {"siminar_id": parseSiminarId()}

        super(BaseSuite, self).__init__(*args, **kwargs)

class KeepSiminar(BaseSuite):
    @classmethod
    def tearDownClass(self):
        print "KeepSimianr tearDown does not erase the Siminar."
