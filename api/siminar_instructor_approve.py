import settings
import unittest
from base import BaseSuite, authorize

class ApproveInstructor(BaseSuite):

    @authorize(settings.INSTRUCTOR_EMAIL, settings.INSTRUCTOR_PASSWORD)
    def test_approve_instructor(self):
        data = {"siminar_id": "137706751194861667818098", "user_id": settings.STUDENT_ID}
        cart_ret = self.post(
            "siminar_users" ,
            data=data, **{"siminar_id": "137706751194861667818098", "role": "instructors"})

if __name__ == '__main__':
    unittest.main()
