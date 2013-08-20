import sys
import unittest
from base import BaseSuite, authorize

SIMINAR_ID = "137698486415898621018098"

class SubscribeUser(BaseSuite):

    @authorize("user1@gmail.com", "jaideep")
    def test_callcart(self):
        cart_ret = self.post(
            "cart" ,
            data={"item_id": SIMINAR_ID})

        cart_ret.update({"finalize": 1})

        ret = self.put(
            "cart",
            data=cart_ret)

if __name__ == '__main__':
    unittest.main()
