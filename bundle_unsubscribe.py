import sys
import unittest
from base import BaseSuite, authorize
BUNDLE_ID = "137698573718494767147020"

class SubscribeUser(BaseSuite):
    #@authorize("user1@siminars.com", "jaideep")
    #def test_getbundle_user(self):
    #    x = Api.call(
    #        self.urls["bundle_users"] % {"bundle_id": BUNDLE_ID, "role": "students"},
    #        data=self.data,
    #        method="GET")
    #    print x

    #@authorize("user1@gmail.com", "jaideep")
    @authorize("dev@simversity.com", "jaideep")
    def test_unsubscribe_user(self):
        x = self.delete(
            "bundle_users",
            data={"user_id": "137698485339789688163702"},
            **{"bundle_id": BUNDLE_ID, "role": "students"})

if __name__ == '__main__':
    unittest.main()
