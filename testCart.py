import settings
import unittest
from simtools.timezone import system_now
from simtools.tcp_pipe import NewPipe
from core.runners import Trash
from core.decorators import authorize

class TestCart(Trash):
    @authorize(settings.INSTRUCTOR_EMAIL, settings.INSTRUCTOR_PASSWORD)
    def test1_mySiminars(self):
        """Siminar should appear in mySiminars Unlaunched List"""
        ret = self.get("siminars")
        self.assertTrue(self.storage["siminar_id"] in ret["siminars"]["unlaunched"])

    @authorize(settings.INSTRUCTOR_EMAIL, settings.INSTRUCTOR_PASSWORD)
    def test2_addStep(self):
        """Add 2 Steps to this Siminar"""
        sret1 = self.post("steps", siminar_id=self.storage["siminar_id"])
        sret2 = self.post("steps", siminar_id=self.storage["siminar_id"])
        siminar = self.get("agora_get", {"object_id": self.storage["siminar_id"]})
        self.assertTrue(siminar["steps_num"] == 2)

    @authorize(settings.STUDENT_EMAIL, settings.STUDENT_PASSWORD)
    def test3_anonymousAccess(self):
        """Student cannot Access this unLaunched Siminar"""
        self.storage["student_id"] = self.current_user_id
        with self.assertRaises(Exception):
            siminar = self.get("siminar", siminar_id=self.storage["siminar_id"])


    @authorize(settings.STUDENT_EMAIL, settings.STUDENT_PASSWORD)
    def test41_nobodyLaunchFail(self):
        """Student Cannot Launch this Siminar"""
        with self.assertRaises(Exception):
            self.put("siminar",
                     data={"changed_data": {"status": 12}},
                     siminar_id=self.storage["siminar_id"])

    @authorize(settings.INSTRUCTOR_EMAIL, settings.INSTRUCTOR_PASSWORD)
    def test42_facilitatorLaunch(self):
        """Instructor Launched the Siminar"""
        self.put("siminar",
                 data={"changed_data": {"status": 12}},
                 siminar_id=self.storage["siminar_id"])

    @authorize(settings.STUDENT_EMAIL, settings.STUDENT_PASSWORD)
    def test5_nobodyAccess(self):
        """Siminars can be accessed by Non members"""
        siminar = self.get("siminar", siminar_id=self.storage["siminar_id"])
        self.assertTrue(siminar["siminar"]["user_is_nobody"], True)

    @authorize(settings.STUDENT_EMAIL, settings.STUDENT_PASSWORD)
    def test61_nonFacilitatorDeleteFailure(self):
        """Student Cannot delete this Siminar"""
        siminar_id = self.storage["siminar_id"]
        with self.assertRaises(Exception):
            self.delete("agora_delete", data={"object_ids": [siminar_id]})

    @authorize(settings.STUDENT_EMAIL, settings.STUDENT_PASSWORD)
    def test62_addToFacilitatorFailure(self):
        """Instructor Deletes the Siminar"""
        siminar_id = self.storage["siminar_id"]
        with self.assertRaises(Exception):
            self.post("siminar_users",
                      data={"user_id": self.storage["student_id"]},
                      siminar_id=siminar_id,
                      role="instructors")

    @authorize(settings.INSTRUCTOR_EMAIL, settings.INSTRUCTOR_PASSWORD)
    def test63_addToFacilitators(self):
        """Instructor Adds User to the Siminar"""
        siminar_id = self.storage["siminar_id"]
        self.post("siminar_users",
                  data={"user_id": self.storage["student_id"]},
                  siminar_id=siminar_id,
                  role="instructors")

    @authorize(settings.STUDENT_EMAIL, settings.STUDENT_PASSWORD)
    def test64_studentSiminars(self):
        """
        Siminar shows in Students's Facilitating Siminars.
        """
        ret = self.get("siminars")
        self.assertTrue(self.storage["siminar_id"] in ret["siminars"]["facilitating"])

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCart)
    unittest.TextTestRunner(descriptions=True, verbosity=2).run(suite)

