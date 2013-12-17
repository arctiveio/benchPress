import unittest

from simtools.uploader import UploaderException
from simtools.uploader.external_tools import validate_url
from simtools.uploader.external_tools import guess_content_type

class TestToken(unittest.TestCase):
    valid_video = "http://clips.vorwaerts-gmbh.de/big_buck_bunny.mp4"
    invalid_video = "http://google.com"
    invalid_video_without_protocol = "google.com"
    non_existent_url = "http://www.promod.jhg/"

    tmp_path = "/tmp/hello.txt"
    tmp_content_type = "text/plain"

    def test_404_video(self):
        with self.assertRaises(IOError):
            validate_url(self.non_existent_url, "video")

    def test_invalid_video(self):
        with self.assertRaises(UploaderException):
            validate_url(self.invalid_video, "video")

    def test_invalid_video_without_protocol(self):
        with self.assertRaises(UploaderException):
            validate_url(self.invalid_video_without_protocol, "video")

    def test_valid_video(self):
        self.assertTrue(validate_url(self.valid_video, "video"))

    def test_valid_size(self):
        self.assertTrue(validate_url(self.valid_video, maxsize=5510880))

    def test_invalid_size(self):
        with self.assertRaises(UploaderException):
            validate_url(self.valid_video, maxsize=5510000)

    def test_guess_content_type_filebody(self):
        temp_file = open(self.tmp_path, "w")
        temp_file.writelines(["Hello", "World"])
        temp_file.close()

        temp_file = open(self.tmp_path, "r")
        self.assertEquals(guess_content_type(temp_file), self.tmp_content_type)
        temp_file.close()

    def test_guess_content_type_filepath(self):
        temp_file = open(self.tmp_path, "w")
        temp_file.writelines(["Hello", "World"])
        temp_file.close()

        self.assertEquals(
            guess_content_type(self.tmp_path),
            self.tmp_content_type)

if __name__ == '__main__':
    unittest.main(verbosity=2)
