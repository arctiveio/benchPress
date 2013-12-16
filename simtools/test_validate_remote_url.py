import unittest

from simtools.uploader.external_tools import validate_url
from simtools.uploader import UploaderException

class TestToken(unittest.TestCase):
    valid_video = "http://clips.vorwaerts-gmbh.de/big_buck_bunny.mp4"
    invalid_video = "http://google.com"
    non_existent_url = "http://www.promod.jhg/"

    def test_404_video(self):
        with self.assertRaises(IOError):
            validate_url(self.non_existent_url, "video")
    
    def test_invalid_video(self):
        with self.assertRaises(UploaderException):
            validate_url(self.invalid_video, "video")

    def test_valid_video(self):
        self.assertTrue(validate_url(self.valid_video, "video"))

    def test_valid_size(self):
        self.assertTrue(validate_url(self.valid_video, maxsize=5510880))

    def test_invalid_size(self):
        with self.assertRaises(UploaderException):
            validate_url(self.valid_video, maxsize=5510000)

    #def test_month_long_expiry(self):
    #    pass

    #def test_expired_token(self):
    #    pass

    #def test_valid_token(self):
    #    pass

if __name__ == '__main__':
    unittest.main(verbosity=2)
