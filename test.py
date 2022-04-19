import unittest

from api.dogeApi import DogeApi


class TestDogeApi(unittest.TestCase):
    def test_listCerts(self):
        access_key = "REPLACE_WITH_AccessKey"
        access_token = "REPLACE_WITH_AccessToken"
        res = DogeApi('https://api.dogecloud.com', access_key, access_token) \
            .request("GET", "/cdn/cert/list.json")
        print(res.json())
        self.assertTrue(res.json()['code'] == 200)


if __name__ == '__main__':
    unittest.main()
