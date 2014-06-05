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
        data = {"bundle_id": settings.BUNDLE_ID, "approve": settings.STUDENT_ID}
        cart_ret = self.put(
            "bundle_users" ,
            data=data, **{"bundle_id": settings.BUNDLE_ID, "role": "students"})


if __name__ == '__main__':
    unittest.main()
