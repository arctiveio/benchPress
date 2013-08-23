import settings
import unittest
from simtools.timezone import system_now
from simtools.tcp_pipe import NewPipe
from core.runners import ExistingSiminar

class TestSiminarFlow(ExistingSiminar):
    def test_debug(self):
        print "Testing"

    def test_debug2(self):
        print "Testing2"

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSiminarFlow)
    unittest.TextTestRunner(descriptions=True, verbosity=2).run(suite)

