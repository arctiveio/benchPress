import sys
import unittest
from base import BaseSuite, authorize

SIMINAR_ID = "137698486415898621018098"

class SubscribeUser(BaseSuite):

    @authorize("dev@simversity.com", "jaideep")
    def test_unsubscribe(self):
        ret = self.delete(
            "siminar_users",
            data={"user_id": "137698485339789688163702"},
            **{"siminar_id": SIMINAR_ID, "role": "students"})

if __name__ == '__main__':
    unittest.main()
