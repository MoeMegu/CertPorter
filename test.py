import unittest
from datetime import datetime, tzinfo

import yaml
from OpenSSL import crypto

from api.DogeApi import DogeApi
from utils.AcmeDeliverClient import AcmeDeliverClient


class TestDogeApi(unittest.TestCase):
    cfg: dict
    with open('config.yml', 'r', encoding='utf-8') as cfg_file:
        cfg = yaml.load(cfg_file, Loader=yaml.FullLoader)
    def test_listCerts(self):
        res = DogeApi("AccessKey", "SecretKey", proxies={"https": "http://127.0.0.1:7890"}) \
            .request("GET", "/cdn/cert/list.json")
        print(res.json())
        self.assertEqual(res.json()['code'], 200)

    def test_uploadCerts(self):
        with open('config.yml', 'r', encoding='utf-8') as cfg_file:
            cfg = yaml.load(cfg_file, Loader=yaml.FullLoader)
        ad = AcmeDeliverClient(cfg['acmeDeliver']['host'], cfg['acmeDeliver']['passwd'])
        pub = ad.getCert(cfg['cert-list'][0]['domain'],
                         cfg['cert-list'][0]['pub'], )
        key = ad.getCert(cfg['cert-list'][0]['domain'],
                         cfg['cert-list'][0]['key'])
        print(pub.decode())
        data = {
            "note": cfg['cert-list'][0]['domain'],
            "cert": pub.decode(),
            "private": key.decode()
        }
        # res = DogeApi(cfg['dogecloud']['access_id'], cfg['dogecloud']['secret_key']) \
        #     .request("POST", "/cdn/cert/upload.json", data)
        res = DogeApi(cfg['dogecloud']['access_id'], cfg['dogecloud']['secret_key'], proxies={"https": "http://127.0.0.1:7890"}).uploadCert(data)
        print(res.json())
        self.assertEqual(res.json()['code'], 200)

    def test_getUserInfo(self):
        # res = DogeApi(self.cfg['dogecloud']['access_id'], self.cfg['dogecloud']['secret_key'], proxies={"https": "http://127.0.0.1:7890"}).getUserInfo()
        res = DogeApi(self.cfg['dogecloud']['access_id'], self.cfg['dogecloud']['secret_key'],
                      proxies={"https": "http://127.0.0.1:7890"}).getUserInfo()
        print(res.json()['data'])
        print("已获取到用户信息[UID:{uid}, 用户名:{nickname}]".format(**res.json()['data']))
        for domain in self.cfg['cert-list']:
            print(domain)
        test = print('1') if False else print('2')

class TestAcmeDeliver(unittest.TestCase):
    cfg: dict
    with open('config.yml', 'r', encoding='utf-8') as cfg_file:
        cfg = yaml.load(cfg_file, Loader=yaml.FullLoader)

    def test_getCert(self):
        res = AcmeDeliverClient("REPLACE_WITH_HOST", "REPLACE_WITH_PASS") \
            .getCert("REPLACE_WITH_DOMAIN", "REPLACE_WITH_FILE", )
        self.assertEqual(res.status_code, 200)
        print(res.content.decode())

    def test_getTime(self):
        res = AcmeDeliverClient(self.cfg['acmeDeliver']['host'],
                                self.cfg['cert-list'][0]['passwd'], ).getCert(self.cfg['cert-list'][0]['domain'],
                                                                              "time.log")
        print(res)

    def test_verifyCert(self):
        pub = crypto.load_certificate(crypto.FILETYPE_PEM, AcmeDeliverClient(self.cfg['source']['acmeDeliver']['host'],
                                                                             self.cfg['cert-list'][0]['passwd'], ) \
                                      .getCert(self.cfg['cert-list'][0]['name'], self.cfg['cert-list'][0]['pub']))
        pub.has_expired()
        print(datetime.strptime(str(pub.get_notAfter().decode()).strip('Z'),"%Y%m%d%H%M%S")==datetime.utcfromtimestamp(1655164799))

class TestCfg(unittest.TestCase):
    cfg: dict
    with open('config.yml', 'r', encoding='utf-8') as cfg_file:
        cfg = yaml.load(cfg_file, Loader=yaml.FullLoader)

    def test_loadYaml(self):
        # print(cfg)
        # for domain in cfg['cert-list']:
        #     print(domain)
        # print(cfg['source']['acmeDeliver']['host'])
        # print(cfg['cert-list'])
        print(type(self.cfg))
        print(self.cfg['cert-list'][0]['name0'])
        if self.cfg['cert-list'][0] is None:
            print('e')

    def test_it_domains(self):
        # 生成证书域名交集测试用例
        remote_domain_list: dict
        with DogeApi(self.cfg['dogecloud']['access_id'], self.cfg['dogecloud']['secret_key']).listDomain() as res:
            # print(res.json())
            for n in self.cfg['dogecloud']['cert-domain']:
                print(n)
            for n in res.json()['data']['domains']:
                print(n['name'])

            print(list(self.cfg['dogecloud']['cert-domain'].keys()))
            print(list(filter(lambda x: x['name'] in list(self.cfg['dogecloud']['cert-domain'].keys()),
                              res.json()['data']['domains'])))
            self.remote_domain_list = \
                [d for d in res.json()['data']['domains'] if d["name"] in self.cfg['dogecloud']['cert-domain'].key()]
        print(self.remote_domain_list)


if __name__ == '__main__':
    unittest.main()
