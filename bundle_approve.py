import sys
import unittest
from base import BaseSuite, authorize

BUNDLE_ID = "137698573718494767147020"

class SubscribeUser(BaseSuite):
    #@authorize("user1@siminars.com", "jaideep")
    #def test_getbundle_user(self):
    #    x = self.get(
    #        "bundle_users",
    #        **{"bundle_id": BUNDLE_ID, "role": "students"})
    #    print x

    @authorize("dev@simversity.com", "jaideep")
    def test_callcart(self):
        data = {"bundle_id": BUNDLE_ID, "approve": "137698485339789688163702"}
        cart_ret = self.put(
            "bundle_users" ,
            data=data, **{"bundle_id": BUNDLE_ID, "role": "students"})


if __name__ == '__main__':
    unittest.main()
