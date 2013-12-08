import unittest

from simtools.one_time_token import generate_token, validate_token

from simtools.one_time_token import today, get_offset
from simtools.school import make_md5_password

class TestToken(unittest.TestCase):
    salt = "user_id"

    def test_year_expiry_fail(self):
        with self.assertRaises(ValueError):
            generate_token(self.salt, 31)

    def test_month_long_expiry(self):
        token = generate_token(self.salt, 1)
        self.assertTrue(validate_token(token, self.salt, 30))

    def test_expired_token(self):
        validity = -1
        token = make_md5_password(today()+get_offset(validity), self.salt)
        self.assertFalse(validate_token(token, self.salt, validity=5))

    def test_valid_token(self):
        validity = 2

        token = generate_token(self.salt, validity=validity)
        self.assertTrue(validate_token(token, self.salt, validity))

if __name__ == '__main__':
    unittest.main(verbosity=2)
