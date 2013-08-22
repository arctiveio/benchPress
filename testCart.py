import settings
import unittest
from simtools.timezone import system_now
from simtools.tcp_pipe import NewPipe
from base import BaseSuite, authorize

class TestCart(BaseSuite):
    @authorize(settings.INSTRUCTOR_EMAIL, settings.INSTRUCTOR_PASSWORD)
    def test1CreateSiminar(self):
        ret = self.post(
            "siminars",
            data={
                "title": "Siminar Created on %s" % system_now().strftime("%c")
            })

        self.storage["siminar_id"] = ret.get("created")
        self.assertTrue(self.storage["siminar_id"] is not None)

    @authorize(settings.INSTRUCTOR_EMAIL, settings.INSTRUCTOR_PASSWORD)
    def test2GetSiminar(self):
        ret = self.get("siminars")
        self.assertTrue(self.storage["siminar_id"] in ret["siminars"]["unlaunched"])

    @authorize(settings.INSTRUCTOR_EMAIL, settings.INSTRUCTOR_PASSWORD)
    def test3AddStep(self):
        sret1 = self.post("steps", siminar_id=self.storage["siminar_id"])
        sret2 = self.post("steps", siminar_id=self.storage["siminar_id"])
        siminar = self.get("agora_get", {"object_id": self.storage["siminar_id"]})
        self.assertTrue(siminar["steps_num"] == 2)

    @authorize(settings.STUDENT_EMAIL, settings.STUDENT_PASSWORD)
    def test4AccessUnlaunchedSiminar(self):
        with self.assertRaises(Exception):
            siminar = self.get("siminar", siminar_id=self.storage["siminar_id"])


    @authorize(settings.STUDENT_EMAIL, settings.STUDENT_PASSWORD)
    def test5StudentCannotLaunch(self):
        with self.assertRaises(Exception):
            self.put("siminar",
                     data={"changed_data": {"status": 12}},
                     siminar_id=self.storage["siminar_id"])

    @authorize(settings.INSTRUCTOR_EMAIL, settings.INSTRUCTOR_PASSWORD)
    def test6InstructorCanLaunch(self):
        self.put("siminar",
                 data={"changed_data": {"status": 12}},
                 siminar_id=self.storage["siminar_id"])

    @authorize(settings.STUDENT_EMAIL, settings.STUDENT_PASSWORD)
    def test7AccessLaunchedSiminar(self):
        siminar = self.get("siminar", siminar_id=self.storage["siminar_id"])
        self.assertTrue(siminar["siminar"]["user_is_nobody"], True)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCart)
    unittest.TextTestRunner(verbosity=2).run(suite)

