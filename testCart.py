import settings
import unittest
from simtools.tcp_pipe import NewPipe
from base import BaseSuite, authorize

class TestCart(BaseSuite):
    @authorize("piyush+Piyush1@simversity.com", "Sahara")
    def test_create_siminar(self):
        self.post("siminars", data={"title": "Test SIminar"})

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCart)
    unittest.TextTestRunner(verbosity=2).run(suite)

