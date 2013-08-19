import sys
import unittest
from os.path import abspath, dirname, join

PATH = abspath(dirname(__file__))
sys.path.append(join(PATH, '..'))
from caller import Api, authtoken

USER_ID = "137641111473158486763702"
BUNDLE_ID = "137311548456998639047020"

class SubscribeUser(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        self.urls = Api.get_urls()
        self.email = "user14@siminars.com"
        self.password = "jaideep"
        self.data = {}
        super(SubscribeUser, self).__init__(*args, **kwargs)

    @authtoken("user14@siminars.com", "jaideep")
    def test_getbundle_user(self):
        x = Api.call(
            self.urls["bundle_users"] % {"bundle_id": BUNDLE_ID, "role": "students"},
            data=self.data,
            method="GET")
        print x

    @authtoken("user14@siminars.com", "jaideep")
    def test_callcart(self):
        self.data.update({"item_id": BUNDLE_ID})
        cart_ret = Api.call(
            self.urls["cart"] ,
            data=self.data,
            method="POST")

        self.data.update(cart_ret)
        self.data.update({"finalize": 1})

        ret = Api.call(
            self.urls["cart"] ,
            data=self.data,
            method="PUT")

if __name__ == '__main__':
    unittest.main()
