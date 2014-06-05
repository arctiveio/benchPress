import unittest
import settings
from base import BaseSuite, authorize

class SubscribeUser(BaseSuite):
    #@authorize("user1@siminars.com", "jaideep")
    #def test_getbundle_user(self):
    #    x = self.get(
    #        "bundle_users",
    #        **{"bundle_id": BUNDLE_ID, "role": "students"})
    #    print x

    @authorize(settings.INSTRUCTOR_EMAIL, settings.INSTRUCTOR_PASSWORD)
    def test_callcart(self):
        data = {"siminar_id": settings.SIMINAR_ID, "approve": settings.STUDENT_ID}
        cart_ret = self.put(
            "siminar_users" ,
            data=data, **{"siminar_id": settings.SIMINAR_ID, "role": "students"})


if __name__ == '__main__':
    unittest.main()
