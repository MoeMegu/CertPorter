import unittest

import yaml

from api.DogeApi import DogeApi
from utils.AcmeDeliverClient import AcmeDeliverClient


class TestDogeApi(unittest.TestCase):
    def test_listCerts(self):
        res = DogeApi("AccessKey", "SecretKey") \
            .request("GET", "/cdn/cert/list.json")
        print(res.json())
        self.assertEqual(res.json()['code'], 200)

    def test_uploadCerts(self):
        try:
            with open('config.yml', 'r', encoding='utf-8') as cfg_file:
                cfg = yaml.load(cfg_file, Loader=yaml.FullLoader)
        finally:
            pass
        pem = AcmeDeliverClient(cfg['source']['acmeDeliver']['host'],
                                cfg['cert-list'][0]['name'],
                                cfg['cert-list'][0]['pem'],
                                cfg['source']['acmeDeliver']['passwd']) \
            .getCert()
        key = AcmeDeliverClient(cfg['source']['acmeDeliver']['host'],
                                cfg['cert-list'][0]['name'],
                                cfg['cert-list'][0]['key'],
                                cfg['source']['acmeDeliver']['passwd']) \
            .getCert()
        print(pem.decode())
        data = {
            "note": cfg['cert-list'][0]['name'],
            "cert": pem.decode(),
            "private": key.decode()
        }
        res = DogeApi(cfg['dogecloud']['access_id'], cfg['dogecloud']['secret_key']) \
            .request("POST", "/cdn/cert/upload.json", data)
        print(res.json())
        self.assertEqual(res.json()['code'], 200)


class TestAcmeDeliver(unittest.TestCase):
    def test_getCert(self):
        res = AcmeDeliverClient("REPLACE_WITH_HOST", "REPLACE_WITH_DOMAIN", "REPLACE_WITH_FILE", "REPLACE_WITH_PASS") \
            .getCert()
        self.assertEqual(res.status_code, 200)
        print(res.content.decode())


class TestCfg(unittest.TestCase):
    def test_loadYaml(self):
        cfg_file = open('config.yml', 'r', encoding='utf-8')
        cfg = yaml.load(cfg_file, Loader=yaml.FullLoader)
        cfg_file.close()
        # print(cfg)
        # for domain in cfg['cert-list']:
        #     print(domain)
        # print(cfg['source']['acmeDeliver']['host'])
        # print(cfg['cert-list'])
        print(type(cfg))
        print(cfg['cert-list'][0]['name0'])
        if cfg['cert-list'][0] is None:
            print('e')


if __name__ == '__main__':
    unittest.main()
