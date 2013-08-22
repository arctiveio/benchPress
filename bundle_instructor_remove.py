import settings
import unittest
from base import BaseSuite, authorize

class ApproveInstructor(BaseSuite):

    @authorize(settings.INSTRUCTOR_EMAIL, settings.INSTRUCTOR_PASSWORD)
    def test_remove_instructor(self):
        data = {"user_id": }
        cart_ret = self.delete(
            "bundle_users" ,
            data=data, **{"bundle_id": "137698573718494767147020", "role": "instructors"})

if __name__ == '__main__':
    unittest.main()
