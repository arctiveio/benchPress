import unittest

from simtools.school import ObjectId, \
        generate_oid_string, \
        generate_oid_from_timestamp

from simtools.timezone import epoch_time

class TestOid(unittest.TestCase):
    RID = "HELLO"

    def test_generate_oid(self):
        oid = generate_oid_string(self.RID)
        self.assertEquals(len(oid), 24)

    def test_convert_oid_fail(self):
        with self.assertRaises(Exception):
            oid = ObjectId()
            our_id = generate_oid_from_timestamp(oid.generation_time, self.RID)

    def test_convert_oid_pass(self):
        oid = ObjectId()
        our_id = generate_oid_from_timestamp(epoch_time(oid.generation_time), self.RID)
        self.assertEquals(len(our_id), 24)

if __name__ == '__main__':
    import logging
    FORMAT = '%(asctime)s %(filename)-8s:%(lineno)s [%(levelname)s] %(message)s'
    logging.basicConfig(format=FORMAT, level=logging.DEBUG)

    unittest.main(verbosity=2)
