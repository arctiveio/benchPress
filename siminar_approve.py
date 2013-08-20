import sys
import unittest
from base import BaseSuite, authorize

SIMINAR_ID = "137698486415898621018098"

class SubscribeUser(BaseSuite):
    #@authorize("user1@siminars.com", "jaideep")
    #def test_getbundle_user(self):
    #    x = self.get(
    #        "bundle_users",
    #        **{"bundle_id": BUNDLE_ID, "role": "students"})
    #    print x

    @authorize("dev@simversity.com", "jaideep")
    def test_callcart(self):
        data = {"siminar_id": SIMINAR_ID, "approve": "137698485339789688163702"}
        cart_ret = self.put(
            "siminar_users" ,
            data=data, **{"siminar_id": SIMINAR_ID, "role": "students"})


if __name__ == '__main__':
    unittest.main()
