import unittest
import settings
from base import BaseSuite, authorize
from simtools.timezone import system_now

class SubscribeUser(BaseSuite):

    #def user_approve(self):
    #    data = {"siminar_id": settings.SIMINAR_ID, "approve": settings.STUDENT_ID}
    #    cart_ret = self.put(
    #        "siminar_users" ,
    #        data=data, **{"siminar_id": settings.SIMINAR_ID, "role": "students"})

    #@authorize(settings.INSTRUCTOR_EMAIL, settings.INSTRUCTOR_PASSWORD)
    #def test_user_approve(self):
    #    pass

    @authorize(settings.INSTRUCTOR_EMAIL, settings.INSTRUCTOR_PASSWORD)
    def test_create_siminar(self):
        ret = self.post(
            "siminars",
            data={
                "title": "Siminar Created on %s" % system_now().strftime("%c")
            })

        self.storage["siminar_id"] = ret.get("created")
        self.assertTrue(self.storage["siminar_id"] is not None)

    #@authorize(settings.INSTRUCTOR_EMAIL, settings.INSTRUCTOR_PASSWORD)
    #def test_get_siminar(self):
    #    ret = self.get(
    #        "siminar" ,
    #        **{"siminar_id": self.storage["siminar_id"]})

    #    self.storage["siminar"] = ret.get("siminar")
    #    self.assertEqual(self.storage["siminar_id"], ret["siminar"]["_id"])

    @authorize(settings.STUDENT_EMAIL, settings.STUDENT_PASSWORD)
    def test_user_signup(self):
        cart_ret = self.post(
            "cart" ,
            data={"item_id": self.storage["siminar_id"]})

        cart_ret.update({"finalize": 1})

        ret = self.put(
            "cart",
            data=cart_ret)

        self.assertEqual(self.storage["siminar_id"], ret.get("siminar_id"))
        self.assertTrue(ret.get("paid"))

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(SubscribeUser)
    unittest.TextTestRunner(verbosity=2).run(suite)
