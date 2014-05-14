import unittest
import string
import random

from simtools.uhttpclient import BlockingHTTPClient

class TestClickbankAccounts(unittest.TestCase):
    test_account_id = None
    HOST = "http://192.168.33.10:8032"

    def setUp(self):
        self.conn = BlockingHTTPClient(self.HOST)


    def id_generator(self, size=6):
        chars = string.ascii_uppercase + string.digits
        return ''.join(random.choice(chars) for _ in range(size))


    def test_1_create_account(self):
        test_document = {
            "title": self.id_generator(6),
            "secret_key": self.id_generator(15),
            "api_key": self.id_generator(15),
            "developer_key": self.id_generator(15)
        }

        out = self.conn("/clickbank_accounts", None, data=test_document, method="POST")
        self.__class__.test_account_id = out["data"]["data"]["created"]
        self.assertTrue(self.test_account_id.endswith("35829"))


    def test_2_get_accounts(self):
        out = self.conn("/clickbank_accounts", None, data={}, method="GET")
        self.assertTrue(
            self.test_account_id in \
            map(lambda i: i["_id"], out["data"]["data"]["accounts"]))


    def test_3_get_account(self):
        out = self.conn("/clickbank_account/%s" % self.test_account_id, None, data={}, method="GET")
        self.assertTrue(out["data"]["data"]["account"]["_id"] == self.test_account_id)

    def test_4_edit_account(self):
        data = {"changed_data": {
            "title": self.id_generator(6),
            "secret_key": self.id_generator(6),
            "api_key": self.id_generator(6)
        }}

        out = self.conn("/clickbank_account/%s" % self.test_account_id, None, data=data, method="PUT")
        self.assertTrue(out["data"]["data"]["edited"] is True)


    def test_5_edit_account_no_change(self):
        data = {"changed_data": {}}
        out = self.conn("/clickbank_account/%s" % self.test_account_id, None, data=data, method="PUT")
        self.assertTrue(out["data"]["data"]["edited"] is False)


    def test_6_delete_account(self):
        out = self.conn("/clickbank_account/%s" % self.test_account_id, None, data={}, method="DELETE")
        self.assertTrue(out["data"]["data"]["deleted"] is True)


if __name__ == '__main__':
    import logging
    FORMAT = '%(filename)-8s:%(lineno)s [%(levelname)s] %(message)s'
    logging.basicConfig(format=FORMAT, level=logging.DEBUG)

    unittest.main(verbosity=2)
