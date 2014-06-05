import unittest
from simtools.tcp_pipe import Fetch

class SubPubPipe(unittest.TestCase):
    def test_fail(self):
        x = Fetch("/tmp/subpub.sock", "/can-view")
        print x

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(SubPubPipe)
    unittest.TextTestRunner(verbosity=2).run(suite)
