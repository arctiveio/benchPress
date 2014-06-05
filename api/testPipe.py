import unittest
from simtools.tcp_pipe import NewPipe

class TestPipe(unittest.TestCase):
    def setUp(self):
        self.seq = range(10)

    def test_1_absolute_url_fails(self):
        x = NewPipe("/tmp/subpub.sock")
        with self.assertRaises(Exception):
            x.append("urls")
            x.send(async=False)

    def test_2_non_pipe_non_async_fails(self):
        x = NewPipe("/tmp/subpub.sock")
        x.append("/urls")
        x.append("/urls", data={"check": True})
        with self.assertRaises(Exception):
            x.send(async=False)

    def test_3_pipe_output(self):
        x = NewPipe("/tmp/subpub.sock", is_pipe_supported=True)
        x.append("/urls")
        x.append("/urls", data={"check": True})
        out = x.send()
        self.assertTrue(out["code"], 200)

    def test_4_mutli_source(self):
        x = NewPipe("multi-source", is_pipe_supported=False)
        x.append("/", host="http://macbook.com", datatype="html")
        x.append("/", host="http://moneet.com", datatype="html")
        out = x.send()
        self.assertEqual(out[0]["error"], False)
        self.assertEqual(out[1]["error"], False)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestPipe)
    unittest.TextTestRunner(verbosity=2).run(suite)
