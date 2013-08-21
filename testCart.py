import settings
import unittest
from simtools.timezone import system_now
from simtools.tcp_pipe import NewPipe
from base import BaseSuite, authorize

class TestCart(BaseSuite):
    @authorize(settings.STUDENT_EMAIL, settings.STUDENT_PASSWORD)
    def test1CreateSiminar(self):
        ret = self.post(
            "siminars",
            data={
                "title": "Siminar Created on %s" % system_now().strftime("%c")
            })

        self.storage["siminar_id"] = ret.get("created")
        self.assertTrue(self.storage["siminar_id"] is not None)

    @authorize(settings.STUDENT_EMAIL, settings.STUDENT_PASSWORD)
    def test2GetSiminar(self):
        ret = self.get("siminars")
        self.assertTrue(self.storage["siminar_id"] in ret["siminars"]["unlaunched"])

    @authorize(settings.STUDENT_EMAIL, settings.STUDENT_PASSWORD)
    def test3AddStep(self):
        ret = self.post("steps", siminar_id=self.storage["siminar_id"])
        import pprint; pprint.pprint(ret)
        siminar = self.get("agora_get", {"object_id": self.storage["siminar_id"]})
        import pprint; pprint.pprint(siminar)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCart)
    unittest.TextTestRunner(verbosity=2).run(suite)

