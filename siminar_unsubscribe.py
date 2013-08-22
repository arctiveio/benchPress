import unittest
import settings
from base import BaseSuite, authorize

class SubscribeUser(BaseSuite):

    @authorize(settings.INSTRUCTOR_EMAIL, settings.INSTRUCTOR_PASSWORD)
    def test_unsubscribe(self):
        ret = self.delete(
            "siminar_users",
            data={"user_id": settings.STUDENT_ID},
            **{"siminar_id": settings.SIMINAR_ID, "role": "students"})

if __name__ == '__main__':
    unittest.main()
