import unittest
import settings
from base import BaseSuite, authorize

class SubscribeUser(BaseSuite):
    #@authorize("user1@siminars.com", "jaideep")
    #def test_getbundle_user(self):
    #    x = Api.call(
    #        self.urls["bundle_users"] % {"bundle_id": BUNDLE_ID, "role": "students"},
    #        data=self.data,
    #        method="GET")
    #    print x

    @authorize(settings.INSTRUCTOR_EMAIL, settings.INSTRUCTOR_PASSWORD)
    def test_unsubscribe_user(self):
        x = self.delete(
            "bundle_users",
            data={"user_id": settings.STUDENT_ID},
            **{"bundle_id": settings.BUNDLE_ID, "role": "students"})

if __name__ == '__main__':
    unittest.main()
