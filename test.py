import unittest

from api.dogeApi import DogeApi
from client.AcmeDeliverClient import AcmeDeliverClient


class TestDogeApi(unittest.TestCase):
    def test_listCerts(self):
        access_key = "REPLACE_WITH_AccessKey"
        access_token = "REPLACE_WITH_AccessToken"
        res = DogeApi('https://api.dogecloud.com', access_key, access_token) \
            .request("GET", "/cdn/cert/list.json")
        print(res.json())
        self.assertEqual(res.json()['code'], 200)


class TestAcmeDeliver(unittest.TestCase):
    def test_getCert(self):
        res = AcmeDeliverClient("REPLACE_WITH_HOST", "REPLACE_WITH_DOMAIN","REPLACE_WITH_FILE","REPLACE_WITH_PASS") \
            .getCert()
        self.assertEqual(res.status_code, 200)
        print(res.content.decode())


if __name__ == '__main__':
    unittest.main()
