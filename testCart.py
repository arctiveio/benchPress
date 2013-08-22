import settings
import unittest
from simtools.timezone import system_now
from simtools.tcp_pipe import NewPipe
from base import BaseSuite, authorize

class TestCart(BaseSuite):
    @authorize(settings.INSTRUCTOR_EMAIL, settings.INSTRUCTOR_PASSWORD)
    def test1(self):
        """Create a Siminar"""
        ret = self.post(
            "siminars",
            data={
                "title": "Siminar Created on %s" % system_now().strftime("%c")
            })

        self.storage["siminar_id"] = ret.get("created")
        self.assertTrue(self.storage["siminar_id"] is not None)

    @authorize(settings.INSTRUCTOR_EMAIL, settings.INSTRUCTOR_PASSWORD)
    def test2(self):
        """Siminar should appear in mySiminars Unlaunched List"""
        ret = self.get("siminars")
        self.assertTrue(self.storage["siminar_id"] in ret["siminars"]["unlaunched"])

    @authorize(settings.INSTRUCTOR_EMAIL, settings.INSTRUCTOR_PASSWORD)
    def test3(self):
        """Add 2 Steps to this Siminar"""
        sret1 = self.post("steps", siminar_id=self.storage["siminar_id"])
        sret2 = self.post("steps", siminar_id=self.storage["siminar_id"])
        siminar = self.get("agora_get", {"object_id": self.storage["siminar_id"]})
        self.assertTrue(siminar["steps_num"] == 2)

    @authorize(settings.STUDENT_EMAIL, settings.STUDENT_PASSWORD)
    def test4(self):
        """Student cannot Access this unLaunched Siminar"""
        with self.assertRaises(Exception):
            siminar = self.get("siminar", siminar_id=self.storage["siminar_id"])


    @authorize(settings.STUDENT_EMAIL, settings.STUDENT_PASSWORD)
    def test5(self):
        """Student Cannot Launch this Siminar"""
        with self.assertRaises(Exception):
            self.put("siminar",
                     data={"changed_data": {"status": 12}},
                     siminar_id=self.storage["siminar_id"])

    @authorize(settings.INSTRUCTOR_EMAIL, settings.INSTRUCTOR_PASSWORD)
    def test6(self):
        """Instructor Launched the Siminar"""
        self.put("siminar",
                 data={"changed_data": {"status": 12}},
                 siminar_id=self.storage["siminar_id"])

    @authorize(settings.STUDENT_EMAIL, settings.STUDENT_PASSWORD)
    def test7(self):
        """Siminars can be accessed by Non members"""
        siminar = self.get("siminar", siminar_id=self.storage["siminar_id"])
        self.assertTrue(siminar["siminar"]["user_is_nobody"], True)

    @authorize(settings.STUDENT_EMAIL, settings.STUDENT_PASSWORD)
    def test8(self):
        """Student Cannot delete this Siminar"""
        siminar_id = self.storage["siminar_id"]
        with self.assertRaises(Exception):
            self.delete("agora_delete", data={"object_ids": [siminar_id]})

    @authorize(settings.INSTRUCTOR_EMAIL, settings.INSTRUCTOR_PASSWORD)
    def test9(self):
        """Instructor Deletes the Siminar"""
        siminar_id = self.storage["siminar_id"]
        self.delete("agora_delete", data={"object_ids": [siminar_id]})

    @authorize(settings.INSTRUCTOR_EMAIL, settings.INSTRUCTOR_PASSWORD)
    def test91(self):
        """Siminar does not show in Instructor's Siminars."""
        ret = self.get("siminars")
        self.assertTrue(self.storage["siminar_id"] not in ret["siminars"]["unlaunched"])
        self.assertTrue(self.storage["siminar_id"] not in ret["siminars"]["facilitating"])

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCart)
    unittest.TextTestRunner(verbosity=2).run(suite)

