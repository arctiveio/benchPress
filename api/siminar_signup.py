import unittest
import settings
from core.runners import TrashSiminar
from core.decorators import authorize
from simtools.timezone import system_now

class SubscribeUser(TrashSiminar):

    @authorize(settings.INSTRUCTOR_EMAIL, settings.INSTRUCTOR_PASSWORD)
    def test11_create_payment_card():
        pass

    @authorize(settings.INSTRUCTOR_EMAIL, settings.INSTRUCTOR_PASSWORD)
    def test_create_siminar(self):
        ret = self.post(
            "siminars",
            data={
                "title": "Siminar Created on %s" % system_now().strftime("%c")
            })

        self.storage["siminar_id"] = ret.get("created")
        print "Created Siminar %s" % self.storage["siminar_id"]
        self.assertTrue(self.storage["siminar_id"] is not None)

    @authorize(settings.INSTRUCTOR_EMAIL, settings.INSTRUCTOR_PASSWORD)
    def test_launch_siminar(self):
        ret = self.put(
            "siminar" ,
            data={"changed_data": {"status": 12}},
            **{"siminar_id": self.storage["siminar_id"]})

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

    @authorize(settings.INSTRUCTOR_EMAIL, settings.INSTRUCTOR_PASSWORD)
    def test_get_siminar(self):
        ret = self.get(
            "siminar" ,
            **{"siminar_id": self.storage["siminar_id"]})

        self.assertEqual(self.storage["siminar_id"], ret["siminar"]["_id"])
        siminar = ret.get("siminar")
        if siminar.get("is_participation_moderated"):
            print "Participation Moderated , so approving user"

    @authorize(settings.INSTRUCTOR_EMAIL, settings.INSTRUCTOR_PASSWORD)
    def approve_user(self):
        data = {"siminar_id": self.storage["siminar_id"], "approve": settings.STUDENT_ID}
        ret = self.put(
            "siminar_users" ,
            data=data, **{"siminar_id": self.storage["siminar_id"], "role": "students"})

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(SubscribeUser)
    unittest.TextTestRunner(verbosity=2).run(suite)
